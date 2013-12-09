from fawnlog import config
from fawnlog import projection
from fawnlog import linkedlist_queue
from fawnlog import seq_to_flash_pb2
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
        return self.cur_ips


class Request(object):
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
        self.start_flash_index = config.FLASH_PER_GROUP * self.group_index
        self.end_flash_index = self.start_flash_index + config.FLASH_PER_GROUP
        self.flash_queue_table = [Queue.Queue()
            for i in range(config.FLASH_PER_GROUP)]

        self.token = start_token
        # self.cursor point to the current flash unit we should write to
        (self.cursor, _, _, _) = projection.translate(self.token)

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
        self.end_flash_index = self.start_flash_index + config.FLAHS_PER_GROUP
        # For requests still in the queue, reply the flash unit is full
        for q in self.flash_queue_table:
            while not q.empty():
                request = q.get()
                self.send_to_flash(request, -1, True)

    def _increase_one(self):
        """Increase token and cursor by one.
        Invariant: the cursor always points to the flash unit which is not
        full and the queue for the flash unit is empty.
        """
        self.token += 1
        self.cursor += 1
        if self.cursor == self.end_flash_index:
            if self._is_full(self.end_flash_index - 1):
                # the last flash unit in the group is full,
                # move to the next group
                self._next_group()
            else:
                self.cursor = self.start_flash_index

    def _increase_to_index(self, flash_unit_index):
        """Increase token to make the cursor point to flash_unit_index.
        If the flash unit pointed by flash_unit_index is full,
        keep the current token and cursor.
        Return True on success.
        Return False if the flash_unix_index is full.
        """
        num = flash_unit_index - self.cursor
        if num < 0:
            num += config.FLASH_PER_GROUP
        token = self.token + num
        (cursor, _, _, _) = projection.translate(token)
        if cursor >= self.end_flash_index:
            # the flash unit group is full
            return False
        else:
            self.token = token
            self.cursor = flash_unit_index

    def _set_global_timer(self):
        self.global_req_timer.cancel()
        if not self.global_req_queue.empty():
            timestamp = self.global_req_queue.head.data.request_timestamp
            interval = config.REQUEST_TIMEOUT - (time.time() - timestamp)
            self.global_req_timer = Timer(interval, self.remove_request)
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
                self.send_to_flash(reuqest, self.token, False)
                self._increase_one()
                q = self.flash_queue_table[self.cursor
                    - self.start_flash_index]
                while not q.empty():
                    node = q.get()
                    self.send_to_flash(node.data, self.token, False)
                    self._remove_from_global(node)
                    slef._increase_one()
                    q = self.flash_queue_table[self.cursor
                        - self.start_flash_index]
            else:
                if not self._is_full(self.token, request.flash_unit_index): 
                    node = self._enqueue_global(request)
                    table_index = fash_unix_index % config.FLASH_PER_GROUP
                    self.flash_queue_table[table_index].put(node)
                else:
                    self.send_to_flash(request, -1, True)
                
    def remove_request(self):
        """Remove request from the head of global_req_queue
        Callback for the global_req_timer.
        """
        with self.lock:
            request = self._global_req_queue.dequeue
            ret = self._increase_to_index(request.flash_unit_index)
            if ret:
                # increase token, create hole
                self.send_to_flash(request, self.token)
                table_index = request.flash_unit_index - self.start_flash_index
                q = self.flash_queue_table[table_index]
                node = q.get()
                if node.request != request:
                    raise RuntimeError(
                        "global_req_queue does not match flash_queue_table.")
            else:
                # the flash group is full
                self.send_to_flash(request, -1, True)
            self._set_global_timer()
        
        
    def reset(self, counter):
        pass

    def send_to_flash(self, request, token, is_full):
        """If is_full is True, token does not have any meaning,
        should be ignored.
        """
        # TODO: need to make asychronous call
        (host, port) = config.SERVER_ADDR_LIST[request.flash_unit_index]
        service_f = RpcService(seq_to_flash_pb2.SeqToFlashService_Stub,
            host, port)
        request_f.data_id = request.data_id
        request_f.token = token
        request_f.request_timestamp = request.request_timestamp
        # timestamp is the timestamp for ips
        request_f.token_timestamp = time.time()
        request_f.ips = self.ips_thread.get_ips()
        request_f.is_full = is_full
        response_f = service.Write(request_f, timeout=10000)

        
