#!/usr/bin/env python2.7
"""Test ips calculation."""

import unittest
import time

from fawnlog import sequencer
from fawnlog import config

INTERVAL = 2 # in seconds

class FakeSequencer(object):
    """
    Fake sequencer class only supports increasing token
    """

    def __init__(self, start_token=0):
        self.token = start_token

    def increase_token(self, num):
        self.token += num

class TestIpsCount(unittest.TestCase):
    """Tests ips count functionality."""

    def test_ips_count(self):
        alpha = config.COUNT_IPS_ALPHA
        seq = FakeSequencer(10)
        ips_thread = sequencer.IpsThread(seq, INTERVAL, alpha)
        ips_thread.start()
        time.sleep(0.5)
        seq.increase_token(100)
        time.sleep(2)
        try:
            self.assertEqual(ips_thread.get_ips(), 50)
            seq.increase_token(50)
            time.sleep(2)
            ips = alpha * 25 + (1 - alpha) * 50 
            self.assertEqual(ips_thread.get_ips(), ips)
        finally:
            ips_thread.stop()
            ips_thread.join()


if __name__ == "__main__":
    unittest.main()
