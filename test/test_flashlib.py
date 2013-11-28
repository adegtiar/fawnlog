#!/usr/bin/env python2.7
"""Tests the flash-writing backend library."""

import os
import multiprocessing.pool
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
        data = self._write_random(0)
        self.assertEqual(data, self.pagefile.read_page(0))

    def test_write_random(self):
        data = self._write_random(5)
        self.assertEqual(data, self.pagefile.read_page(5))

    def test_write_multiple(self):
        data1 = self._write_random(5)
        data2 = self._write_random(20)
        self.assertEqual(data1, self.pagefile.read_page(5))
        self.assertEqual(data2, self.pagefile.read_page(20))

    def test_write_small(self):
        data = self._write_random(0, 10)
        self.assertEqual(data, self.pagefile.read_page(0))

    def test_write_multiple_small(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        self.assertEqual(data1, self.pagefile.read_page(5)[0:10])
        self.assertEqual(data2, self.pagefile.read_page(20)[0:25])

    def test_write_too_big(self):
        self.assertRaises(ValueError, self._write_random, 0, PAGE_SIZE+1)

    def test_persisted(self):
        data = self._write_random(0)
        self.pagefile.close()
        self.setUp()
        self.assertEqual(data, self.pagefile.read_page(0))

    def _write_random(self, offset, size=PAGE_SIZE):
        data = os.urandom(size)
        self.pagefile.write(data, offset)
        return data


class TestPageStore(unittest.TestCase):
    """Tests the PageStore functionality."""

    def setUp(self):
        self.pstore = flashlib.PageStore(TEST_FILE_PATH, PAGE_SIZE)

    def tearDown(self):
        self.pstore.close()
        os.remove(TEST_FILE_PATH)

    def test_write_multiple_small(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        data3 = self._write_random(offset=19)
        self.assertEqual(data1, self.pstore.read(5))
        self.assertEqual(data3, self.pstore.read(19))
        self.assertEqual(data2, self.pstore.read(20))

    def test_overwrite(self):
        self._write_random(offset=5)
        self.assertRaises(flashlib.ErrorOverwritten, self._write_random, 5)

    def test_unwritten_hole(self):
        self._write_random(offset=5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 0)

    def test_unwritten_edge(self):
        self._write_random(offset=0)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 5)

    def test_persisted_init(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        data3 = self._write_random(offset=19)

        self.pstore.close()
        self.setUp()

        self.assertEqual(data1, self.pstore.read(5))
        self.assertEqual(data3, self.pstore.read(19))
        self.assertEqual(data2, self.pstore.read(20))
        self.assertRaises(flashlib.ErrorOverwritten, self._write_random, 5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 1)

    def test_reset(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        data3 = self._write_random(offset=19)

        self.pstore.reset()

        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 20)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 19)

    def test_concurrent_writes(self):
        pool = multiprocessing.pool.ThreadPool(20)
        try:
            data = pool.map(self._write_random, xrange(20))
        finally:
            pool.close()
        read_data = map(self.pstore.read, xrange(20))
        self.assertEqual(data, read_data)

    def test_concurrent_reads(self):
        data = map(self._write_random, xrange(20))
        pool = multiprocessing.pool.ThreadPool(20)
        try:
            read_data = pool.map(self.pstore.read, xrange(20))
        finally:
            pool.close()
        self.assertEqual(data, read_data)

    def test_concurrent_rw(self):
        data = map(self._write_random, xrange(20))
        pool1 = multiprocessing.pool.ThreadPool(20)
        pool2 = multiprocessing.pool.ThreadPool(20)
        try:
            pool1.map_async(self._write_random, xrange(20, 40))
            read_data = pool2.map(self.pstore.read, xrange(20))
        finally:
            pool1.terminate()
            pool2.terminate()
        self.assertEqual(data, read_data)

    def _write_random(self, offset, size=PAGE_SIZE):
        data = os.urandom(size)
        self.pstore.write(data, offset)
        return data


if __name__ == "__main__":
    unittest.main()
