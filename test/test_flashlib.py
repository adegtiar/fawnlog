#!/usr/bin/env python2.7
"""Tests the flash-writing backend library."""

import os
import multiprocessing.pool
import unittest


from fawnlog import flashlib


TEST_FILE_PATH = "pagefile_test.flog"
PAGE_SIZE = 1024
NUM_PAGES = 40000


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


class TestPageStoreBase(object):
    def setUp(self):
        self.pstore = flashlib.PageStore(TEST_FILE_PATH, PAGE_SIZE, NUM_PAGES)

    def tearDown(self):
        self.pstore.close()
        os.remove(TEST_FILE_PATH)

    def _write_random(self, offset, size=PAGE_SIZE):
        data = os.urandom(size)
        self.pstore.write(data, offset)
        return data


class TestPageStoreBasic(TestPageStoreBase, unittest.TestCase):
    """Tests basic PageStore functionality."""

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

    def test_unwritten(self):
        self._write_random(offset=5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 0)

    def test_unwritten_edge(self):
        self._write_random(offset=0)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 5)

    def test_hole_read(self):
        self.pstore.fill_hole(offset=5)
        self.assertRaises(flashlib.ErrorFilledHole, self.pstore.read, 5)

    def test_hole_write(self):
        self.pstore.fill_hole(offset=5)
        self.assertRaises(flashlib.ErrorFilledHole, self._write_random, 5)

    def test_hole_overwritten(self):
        self._write_random(offset=5)
        self.assertRaises(flashlib.ErrorOverwritten, self.pstore.fill_hole, 5)

    def test_persisted_init(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        data3 = self._write_random(offset=19)
        self.pstore.fill_hole(offset=4)
        self.pstore.fill_hole(offset=6)
        self.pstore.fill_hole(offset=10)

        self.pstore.close()
        self.setUp()

        self.assertEqual(data1, self.pstore.read(5))
        self.assertEqual(data3, self.pstore.read(19))
        self.assertEqual(data2, self.pstore.read(20))
        self.assertRaises(flashlib.ErrorOverwritten, self._write_random, 5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 1)

        self.assertRaises(flashlib.ErrorFilledHole, self.pstore.read, 4)
        self.assertRaises(flashlib.ErrorFilledHole, self.pstore.read, 6)
        self.assertRaises(flashlib.ErrorFilledHole, self.pstore.read, 10)

    def test_reset(self):
        data1 = self._write_random(offset=5, size=10)
        data2 = self._write_random(offset=20, size=25)
        data3 = self._write_random(offset=19)

        self.pstore.reset()

        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 5)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 20)
        self.assertRaises(flashlib.ErrorUnwritten, self.pstore.read, 19)


class TestPageStoreConcurrent(TestPageStoreBase, unittest.TestCase):
    """Tests the PageStore concurrent functionality."""

    def setUp(self):
        TestPageStoreBase.setUp(self)
        self.pool1 = multiprocessing.pool.ThreadPool(20)
        self.pool2 = multiprocessing.pool.ThreadPool(20)

    def tearDown(self):
        self.pool1.terminate()
        self.pool2.terminate()
        TestPageStoreBase.tearDown(self)

    def test_concurrent_writes(self):
        data = self.pool1.map(self._write_random, xrange(20))
        read_data = map(self.pstore.read, xrange(20))
        self.assertEqual(data, read_data)

    def test_concurrent_reads(self):
        data = map(self._write_random, xrange(20))
        read_data = self.pool1.map(self.pstore.read, xrange(20))
        self.assertEqual(data, read_data)

    def test_concurrent_rw(self):
        data = map(self._write_random, xrange(20))
        self.pool1.map_async(self._write_random, xrange(20, 40))
        read_data = self.pool2.map(self.pstore.read, xrange(20))
        self.assertEqual(data, read_data)


if __name__ == "__main__":
    unittest.main()
