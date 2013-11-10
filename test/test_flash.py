#!/usr/bin/env python2.7
"""Tests the flash-writing backend library."""

import os
import unittest

from fawnlog import flashlib


TEST_FILE_PATH = "pagefile_test.flog"
PAGE_SIZE = 1024


class TestPageFile(unittest.TestCase):
    """Tests the basic page file functionality."""

    def setUp(self):
        self.pagefile = flashlib.PageFile(TEST_FILE_PATH, PAGE_SIZE)

    def tearDown(self):
        self.pagefile.close()
        os.remove(TEST_FILE_PATH)

    def test_write_basic(self):
        data = os.urandom(PAGE_SIZE)
        self.pagefile.write(data, 0)
        read_data = self.pagefile.read(0)
        self.assertEqual(data, read_data)



if __name__ == "__main__":
    unittest.main()
