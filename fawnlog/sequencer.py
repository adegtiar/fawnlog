from fawnlog import config
from fawnlog import projection

import threading

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

        # used to calculate ips
        self.last_token = start_token
        self.cur_ips = 0
        self.ips_timer = threading.Timer(config.INTERVAL, count_ips)
        self.ips_timer.start()


    def reset(self, counter):
        pass

    def count_ips():
        """Calculate token increments per second, get called by ips_timer."""

        alpha = config.COUNT_IPS_ALPHA
        ips = (self.token - self.last_token) * 1.0 / config.COUNT_IPS_INTERVAL
        # calculate exponential moving average
        self.cur_ips = alpha * ips + (1 - alpha) * self.cur_ips
        self.last_token = self.token

        # reset the timer
        self.ips_timer.start()
