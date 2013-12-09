"""The sequencer.
"""

from fawnlog import config
from fawnlog import projection
from fawnlog import linkedlist_queue
from fawnlog import flash_service_pb2
from protobuf.socketrpc import RpcService

import Queue
import threading
import time

class IpsThread(threading.Thread):
    """
    A thread fires the timer at interval config.COUNT_IPS_INTERVAL
    to calculate increments per second (ips).
    """

    def __init__(self, sequencer, interval=config.COUNT_IPS_INTERVAL):
        super(IpsThread, self).__init__()
        self.sequencer = sequencer
        self.alpha = config.COUNT_IPS_ALPHA
        self.interval = interval
        self.last_token = None
        self.cur_ips = None
        self.stopped = False

    def run(self):
        self.last_token = self.sequencer.token
        threading.Timer(self.interval, self.count_ips).start()

    def stop(self):
        """Stop the repeating timer."""
        self.stopped = True

    def count_ips(self):
        """Calculate token increments per second, get called by ips_timer."""

        ips = (self.sequencer.token - self.last_token) * 1.0 / self.interval
        # calculate exponential moving average
        if self.cur_ips is None:
            self.cur_ips = ips
        else:
            self.cur_ips = self.alpha * ips + (1 - self.alpha) * self.cur_ips
        self.last_token = self.sequencer.token

        # reset the timer
        if not self.stopped:
            threading.Timer(self.interval, self.count_ips).start()

    def get_ips(self):
        """Get current ips."""
        return self.cur_ips


class Request(object):
    """Client request"""

    def __init__(self, data_id, flash_unit_index):
        self.data_id = data_id
        self.flash_unit_index = flash_unit_index
        # when we get the request
        self.request_timestamp = time.time()


class Sequencer(object):
    """
    A simple sequencer which serialize requests and generates tokens.
    """

    def __init__(self, start_token=0):
        self.lock = threading.Lock()

        # current projection
        group_index = start_token // (config.FLASH_PAGE_NUMBER *
            config.FLASH_PER_GROUP)
        self.start_flash_index = config.FLASH_PER_GROUP * group_index
        self.end_flash_index = self.start_flash_index + config.FLASH_PER_GROUP
        self.flash_queue_table = [Queue.Queue()
            for i in range(config.FLASH_PER_GROUP)]

        self.projection = projection.Projection()

        self.token = start_token
        # self.cursor point to the current flash unit we should write to
        (self.cursor, _, _, _) = self.projection.translate(self.token)

        # global request queue
        self.global_req_queue = linkedlist_queue.LinkedListQueue()
        self.global_req_timer = None

        # start calculating ips
        self.ips_thread = IpsThread(self)
        self.ips_thread.start()

    def _is_full(self, flash_unit_index):
        """Check if the flash with flash_unit_index is full"""
        return self.token >= config.FLASH_PAGE_NUMBER * (flash_unit_index + 1)

    def _next_group(self):
        """When this group of flash units are full,
        Move to the next group, the group wraps around (wrong).
        """
        total_flash = len(config.SERVER_ADDR_LIST)
        self.start_flash_index = self.end_flash_index % total_flash
        self.end_flash_index = self.start_flash_index + config.FLASH_PER_GROUP
        self.cursor = self.start_flash_index
        # For requests still in the queue, reply the flash unit is full
        for queue in self.flash_queue_table:
            while not queue.empty():
                request = queue.get()
                self.send_to_flash(request, -1, is_full=True)

    def _increase_by_one(self):
        """Increase token and cursor by one.
        Return True if the group is full, we moved to the next group,
        Return False otherwise
        """
        self.token += 1
        self.cursor += 1
        if self.cursor == self.end_flash_index:
            if self._is_full(self.end_flash_index - 1):
                # the last flash unit in the group is full,
                # move to the next group
                self._next_group()
                return True
            else:
                self.cursor = self.start_flash_index
        return False

    def _adjust_cursor(self):
        """Adjust the cursor to maintain the Invariant:
        The cursor always points to the flash unit
        which is not full and the queue for the flash unit is empty.
        """
        queue = self.flash_queue_table[self.cursor
            - self.start_flash_index]
        while not queue.empty():
            node = queue.get()
            self.send_to_flash(node.data, self.token)
            self._remove_from_global(node)
            self._increase_by_one()
            queue = self.flash_queue_table[self.cursor
                - self.start_flash_index]

    def _increase_to_index(self, flash_unit_index):
        """Increase token to make the cursor point to flash_unit_index.
        Return True if the group is full, we moved to the next group.
        Return False otherwise
        """
        while (self.cursor != flash_unit_index):
            new_group = self._increase_by_one()
            if new_group:
                return True
            queue = self.flash_queue_table[self.cursor
                - self.start_flash_index]
            if queue.empty():
                self.fill_hole_flash(self.token)
            else:
                node = queue.get()
                self._remove_from_global(node)
                self.send_to_flash(node.data, self.token)
        self._increase_by_one()
        node = queue.get()
        self.send_to_flash(node.data, self.token)
        self._adjust_cursor()
        return False

    def _set_global_timer(self):
        """Set global timer for the request at the head of the
        global_seq_queue.
        """
        self.global_req_timer.cancel()
        if not self.global_req_queue.empty():
            timestamp = self.global_req_queue.head.data.request_timestamp
            interval = config.REQUEST_TIMEOUT - (time.time() - timestamp)
            self.global_req_timer = threading.Timer(
                interval, self.remove_request)
            self.global_req_timer.start()

    def _enqueue_global(self, request):
        """Enqueue to the global_req_queue.
        If the queue is initially empty, set the timer.
        """
        node = self.global_req_queue.enqueue(request)
        if self.global_req_queue.length == 1:
            # this is the head, set timer
            self._set_global_timer()
        return node

    def _remove_from_global(self, node):
        """Remove from the global_req_queue.
        If the removed node is the head, set the new timer.
        """
        is_head = False
        if node == self.global_req_queue.head:
            is_head = True
        self.global_req_queue.remove(node)
        if is_head:
            # set timer
            self._set_global_timer()

    def insert_request(self, data_id, flash_unit_index):
        """Insert a new request.
        This should be called by sequencer service.
        """
        request = Request(data_id, flash_unit_index)
        with self.lock:
            if self.cursor == flash_unit_index:
                self.send_to_flash(request, self.token)
                self._increase_by_one()
                self._adjust_cursor()
            else:
                node = self._enqueue_global(request)
                table_index = flash_unit_index % config.FLASH_PER_GROUP
                self.flash_queue_table[table_index].put(node)

    def remove_request(self):
        """Remove request from the head of global_req_queue
        Callback for the global_req_timer.
        """
        with self.lock:
            request = self.global_req_queue.dequeue()
            new_group = self._increase_to_index(request.flash_unit_index)
            if new_group:
                self.send_to_flash(request, -1, is_full=True)
            self._set_global_timer()

    def reset(self, token):
        """Resets the state of the sequencer."""
        pass

    def callback(self, request, response):
        """Async callback which does nothing"""
        pass

    def send_to_flash(self, request, token, is_full=False):
        """If is_full is True, token does not have any meaning,
        should be ignored.
        """
        (host, port) = config.SERVER_ADDR_LIST[request.flash_unit_index]
        # TODO: initialize RpcService in init
        service_f = RpcService(flash_service_pb2.FlashService_Stub,
            host, port)
        request_f = flash_service_pb2.WriteOffsetRequest()
        request_f.data_id = request.data_id
        (_, _, _, request_f.offset) = self.projection.translate(token)
        request_f.is_full = is_full
        request_f.measure.token = token
        request_f.measure.request_timestamp = request.request_timestamp
        # timestamp is the timestamp for ips
        request_f.measure.token_timestamp = time.time()
        request_f.measure.ips = self.ips_thread.get_ips()
        service_f.WriteOffset(request_f, callback=self.callback)

    def fill_hole_flash(self, token):
        """Creates a hole at the token by sending a FillHole request."""
        _, host, port, offset = self.projection.translate(token)

        request_f = flash_service_pb2.FillHoleRequest()
        request_f.offset = offset

        # TODO: initialize RpcService in init
        service_f = RpcService(flash_service_pb2.FlashService_Stub, host, port)
        service_f.FillHole(request_f, callback=self.callback)
