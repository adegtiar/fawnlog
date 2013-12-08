from fawnlog import config
from fawnlog import projection
from fawnlog import linkedlist_queue

import threading

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

class Sequencer(object):
    """
    A simple sequencer which serialize requests and generates tokens.
    """

    def __init__(self, start_token=0):
        self.lock = threading.Lock()

        # current projection
        self.group_index = start_token // (config.FLASH_PAGE_NUMBER *
            config.FLASH_PER_GROUP)

        self.token = start_token
        # self.flash_cursor point to the current flash unit we should write to
        (self.flash_cursor, _, _, _) = projection.translate(self.token)

        # global request queue
        self.global_req_queue = linkedlist_queue.LinkedListQueue()
        self.global_req_timer = None
       
    def reset(self, counter):
        pass
  
