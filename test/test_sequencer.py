#!/usr/bin/env python2.7
"""Tests sequencer."""

import unittest
import time

from fawnlog.sequencer import Sequencer

from test import config

class SequencerCore(Sequencer):

    def __init__(self, start_token=0):
        super(SequencerCore, self).__init__(config, start_token)

    """Override methods so we don't make RPC calls"""
    def send_to_flash(self, request, token, is_full=False):
        pass

    def fill_hole_flash(self, token):
        pass

class TestSequencer(unittest.TestCase):
    """Test the basic sequencer functionality."""

    def test_ideal_world(self):
        """The reqeusts come in order and always guess correctly,
        no timeout should happen.
        """
        sequencer = SequencerCore()
        try:
            for data_id in xrange(config.FLASH_PER_GROUP *
                config.FLASH_PAGE_NUMBER):
                flash_unit_index = data_id % config.FLASH_PER_GROUP
                sequencer.insert_request(str(data_id), flash_unit_index)
                self.assertEqual(sequencer.token, data_id+1)
        finally:
            sequencer.ips_thread.stop()
            sequencer.ips_thread.join()

    def test_next_group(self):
        """The requests come in order and always guess correctly,
        but will move to the next group.
        """
        token = (config.FLASH_PER_GROUP - 1) * config.FLASH_PAGE_NUMBER
        sequencer = SequencerCore(token)
        try:
            for i in xrange(config.FLASH_PAGE_NUMBER):
                data_id = i + token
                flash_unit_index = data_id % config.FLASH_PER_GROUP
                sequencer.insert_request(str(data_id), flash_unit_index)
            self.assertEqual(sequencer.cursor, config.FLASH_PER_GROUP)
        finally:
            sequencer.ips_thread.stop()
            sequencer.ips_thread.join()

    def test_timeout_basic(self):
        """The requests guessed wrong and will timeout,
        we will make a hole for it.
        """
        sequencer = SequencerCore()
        try:
            sequencer.insert_request(str(1), config.FLASH_PER_GROUP-1)
            self.assertEqual(sequencer.token, 0)
            self.assertEqual(sequencer.cursor, 0)
            time.sleep(config.REQUEST_TIMEOUT + 0.01)
            self.assertEqual(sequencer.token, config.FLASH_PER_GROUP)
            self.assertEqual(sequencer.cursor, 0)
            sequencer.insert_request(str(2), config.FLASH_PER_GROUP-1)
            self.assertEqual(sequencer.token, config.FLASH_PER_GROUP)
            time.sleep(config.REQUEST_TIMEOUT + 0.01)
            self.assertEqual(sequencer.token, config.FLASH_PER_GROUP*2)
        finally:
            sequencer.ips_thread.stop()
            sequencer.ips_thread.join()
            if sequencer.global_req_timer is not None:
                sequencer.global_req_timer.cancel()

    @unittest.skip("does not apply anymore")
    def test_adjust_cursor(self):
        """There is a hole in the requests and after that all the requests
        are continuous.
        """
        sequencer = SequencerCore()
        start_index = config.FLASH_PER_GROUP - 1
        try:
            for i in xrange(100):
                data_id = i + start_index
                flash_unit_index = data_id % config.FLASH_PER_GROUP
                sequencer.insert_request(str(data_id), flash_unit_index)
                self.assertEqual(sequencer.cursor, cursor)
        finally:
           sequencer.ips_thread.stop()
           sequencer.ips_thread.join()
           if sequencer.global_req_timer is not None:
               sequencer.global_req_timer.cancel()

if __name__ == "__main__":
    unittest.main()
