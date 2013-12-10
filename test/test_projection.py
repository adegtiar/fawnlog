#!/usr/bin/env python2.7
"""Tests the Projection."""

import unittest

from fawnlog import projection

from test import config

class TestProjection(unittest.TestCase):
    """Tests the basic page file functionality.

        Note passing these tests requires that the first group is full..

    """

    def setUp(self):
        self.projection = projection.Projection(config)
        self.servers = config.SERVER_ADDR_LIST

    def test_translate_basic(self):
        token = 0
        (_, dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[0]
        expect_page = 0
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_round_robin(self):
        token = config.FLASH_PER_GROUP + 1
        (_, dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[1]
        expect_page = 1
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_second_group(self):
        token = config.FLASH_PAGE_NUMBER * config.FLASH_PER_GROUP
        (_, dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[config.FLASH_PER_GROUP]
        expect_page = 0
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_last_page(self):
        number_of_server = len(self.servers)
        token = number_of_server * config.FLASH_PAGE_NUMBER - 1
        (_, dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[number_of_server - 1]
        expect_page = config.FLASH_PAGE_NUMBER - 1
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

if __name__ == "__main__":
    unittest.main()
