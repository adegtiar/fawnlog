#!/usr/bin/env python2.7
"""Tests flash service."""

import os
import random
import unittest

from protobuf.socketrpc import RpcService

import test.helper

from fawnlog import client
from fawnlog import config
from fawnlog import sequencer_service_pb2
from fawnlog import sequencer_service
from fawnlog import flash_service_pb2
from fawnlog import flash_service


class TestEndToEnd(unittest.TestCase):
    """Tests flash service functionality."""

    @classmethod
    def setUpClass(cls):
        # start sequencer
        sequencer_thread = test.helper.ServerThread(config.SEQUENCER_PORT,
            config.SEQUENCER_HOST, sequencer_service.SequencerServiceImpl())
        sequencer_thread.start_server()

        cls.flash_services = []
        for i in xrange(config.FLASH_PER_GROUP):
            cls.flash_services.append(cls._start_flash_server(i))

    @classmethod
    def _start_flash_server(cls, server_index):
        host, port = config.SERVER_ADDR_LIST[server_index]
        server_thread = test.helper.ServerThread(port, host,
                flash_service.FlashServiceImpl.from_index(server_index))
        server_thread.start_server()
        return RpcService(flash_service_pb2.FlashService_Stub, port, host)

    @classmethod
    def _reset_flash_servers(cls):
        for service in cls.flash_services:
            response = service.Reset(flash_service_pb2.ResetRequest())
            assert(response.status == flash_service_pb2.ResetResponse.SUCCESS)

    def setUp(self):
        TestEndToEnd._reset_flash_servers()
        self.test_client = client.Client()

    def test_append_one_short(self):
        """Test writing a short data to one page."""
        self._append_and_assert(config.FLASH_PAGE_SIZE // 100, 1)

    def test_append_one_long(self):
        """Test writing a long data to one page."""
        self._append_and_assert(config.FLASH_PAGE_SIZE - 1, 1)

    def test_append_two_pages(self):
        """Test writing to two pages."""
        self._append_and_assert(config.FLASH_PAGE_SIZE * 2 - 1, 2)

    def test_append_nine_pages(self):
        """Test writing to nine pages."""
        self._append_and_assert(config.FLASH_PAGE_SIZE * 9 - 1, 9)

    def _append_and_assert(self, data_size, expected_num_tokens):
        test_data = os.urandom(data_size)
        return_tokens = self.test_client.append(test_data)
        self.assertEqual(expected_num_tokens, len(return_tokens))
        return_data = [self.test_client.read(token) for token in return_tokens]
        self.assertEqual(test_data, "".join(return_data))

if __name__ == "__main__":
    unittest.main()
