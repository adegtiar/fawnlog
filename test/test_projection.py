#!/usr/bin/env python2.7
"""Tests the Projection."""

import unittest

from fawnlog import config
from fawnlog import projection


class TestProjection(unittest.TestCase):
    """Tests the basic page file functionality."""

    def setUp(self):
        self.projection = projection.Projection()
        self.servers = config.SERVER_ADDR_LIST

    def test_translate_basic(self):
        (dest_host, dest_port, dest_page) = self.projection.translate(0)
        (expect_host, expect_port) = self.servers[0]
        expect_page = 0
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_round_robin(self):
        (dest_host, dest_port, dest_page) = self.projection.translate(3)
        (expect_host, expect_port) = self.servers[1]
        expect_page = 1
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_second_group(self):
        token = 3 + config.FLASH_PAGE_NUMBER * 2
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[3]
        expect_page = 1
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_last_page(self):
        number_of_server = len(self.servers)
        token = number_of_server * config.FLASH_PAGE_NUMBER - 1
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        (expect_host, expect_port) = self.servers[number_of_server - 1]
        expect_page = config.FLASH_PAGE_NUMBER - 1
        self.assertEqual(dest_host, expect_host)
        self.assertEqual(dest_port, expect_port)
        self.assertEqual(dest_page, expect_page)

    def test_translate_half_way_of_last_group(self):
        number_of_server = len(self.servers)
        if number_of_server == 0:
            pass
        else:
            prev_servers = (number_of_server - 1) // 2 * 2
            token = (prev_servers + 1) * config.FLASH_PAGE_NUMBER - 1
            (dest_h, dest_pt, dest_pg) = self.projection.translate(token)
            expect_h, expect_pt, expect_pg = "", 0, 0
            if number_of_server % 2 == 1:
                # no round-robin
                (expect_h, expect_pt) = self.servers[number_of_server - 1]
                expect_pg = config.FLASH_PAGE_NUMBER - 1
            else:
                if config.FLASH_PAGE_NUMBER % 2 == 1:
                    (expect_h, expect_pt) = self.servers[number_of_server - 2]
                    expect_pg = config.FLASH_PAGE_NUMBER // 2
                else:
                    (expect_h, expect_pt) = self.servers[number_of_server - 1]
                    expect_pg = config.FLASH_PAGE_NUMBER // 2 - 1
        self.assertEqual(dest_h, expect_h)
        self.assertEqual(dest_pt, expect_pt)
        self.assertEqual(dest_pg, expect_pg)

if __name__ == "__main__":
    unittest.main()
