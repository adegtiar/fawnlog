class Sequencer(object):
    """
    A simple sequencer which serialize requests and generates tokens. 
    """

    def __init__(self, start=0):
        self.counter = start

    def reset(self, counter):
        self.counter = counter

    def get_token(self, number):
        """Return the current counter and increase it by number"""
        token = self.counter
        for i in range(number):
            self.counter += 1
        return token
