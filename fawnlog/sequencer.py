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
    def __init__(self, data_id, flash_unix_index):
        self.data_id = data_id
        self.flash_unix_index = flash_unix_index
        # when we get the request
        self.timestamp = time.time()

        
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
        # self.flash_cursor point to the current flash unit we should write to
        (self.flash_cursor, _, _, _) = projection.translate(self.token)

        # global request queue
        self.global_req_queue = linkedlist_queue.LinkedListQueue()
        self.global_req_timer = None

        # start calculating ips
        self.ips_thread = IpsThread(self)
        self.ips_thread.start()

    def _is_full(self, token, flash_unit_index):
        """Check if the flash with flash_unit_index is full"""
        return token > config.FLASH_PAGE_NUMBER * (flash_unix_index + 1)

    def _next_group(self):
        # wrap around
        total_flash = len(config.SERVER_ADDR_LIST)
        self.start_flash_index = self.end_flash_index % total_flash
        self.end_flash_index = self.start_flash_index + config.FLAHS_PER_GROUP 

    def _increase(self):
        self.token += 1
        self.cursor += 1
        if self.cursor == self.end_flash_index:
            self.cursor = self.start_flash_index
        if self._is_full(self.token, self.cursor):
            # the flash unit is full, get the next group
            self._next_group()
            self.cursor = self.start_flash_index

    def _set_global_timer(self, node):
        interval = config.REQUEST_TIMEOUT - (time.time() - node.data.timestamp)
        self.global_req_timer = Timer(interval, self.remove_request, node)
        self.global_req_timer.start()

    def _enqueue_global(self, request):
        node = self.global_req_queue.enqueue(request)
        if self.global_req_queue.length == 1:
            # this is the head, set timer
            self._set_global_timer(node)
        return node

    def _remove_from_global(self, node):
        is_head = False
        if node == self.global_req_queue.head:
            is_head = True
        self.global_req_queue.remove(node)
        if is_head:
            # set timer
            self._set_global_timer(self.global_req_queue.head)

    def insert_request(self, data_id, flash_unit_index):
        request = Request(data_id, flash_unit_index)
        with self.lock:
            if self.cursor == flash_unit_index:
                self.send_to_flash(reuqest, self.token)
                self._increase()
                q = self.flash_queue_table[self.cursor
                    - self.start_flash_index]
                while not q.empty():
                    node = q.get()
                    self.send_to_flash(node.data)
                    self._remove_from_global(node)
                    slef._increase()
                    q = self.flash_queue_table[self.cursor
                        - self.start_flash_index]
            else:
                node = self._enqueue_global(request)
                table_index = fash_unix_index % config.FLASH_PER_GROUP
                self.flash_queue_table[table_index].put(node)
                
    def remove_request(self, node):
        pass
        
        
    def reset(self, counter):
        pass

    def send_to_flash(self, request, token):
        (host, port) = config.SERVER_ADDR_LIST[request.flash_unix_index]
        service_f = RpcService(seq_to_flash_pb2.SeqToFlashService_Stub,
            host, port)
        request_f.data_id = request.data_id
        request_f.token = token
        # timestamp is the timestamp for ips
        request_f.timestamp = time.time()
        request_f.ips = self.ips_thread.get_ips()
        response_f = service.Write(request_f, timeout=10000)

        
