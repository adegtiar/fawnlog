import threading

class Sequencer(object):
    """
    A simple sequencer which serialize requests and generates tokens.
    """

    def __init__(self, start=0):
        self.counter = start
        self.lock = threading.Lock()

    def reset(self, counter):
        with self.lock:
            self.counter = counter

    def get_token(self, number):
        """
        param: number: the number of flash pages wants to reserve.
        Return the current counter and increase it by number
        """
        with self.lock:
            token = self.counter
            self.counter += number
        return token
