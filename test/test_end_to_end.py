#!/usr/bin/env python2.7
"""Tests flash service."""

import unittest
import os

from protobuf.socketrpc import RpcService

import test.helper

from fawnlog import get_token_pb2
from fawnlog import get_token_service
from fawnlog import flash_service_pb2
from fawnlog import flash_service

SEQUENCER_PORT = 10001
SEQUENCER_HOST = "127.0.0.1"
FLASH_SERVER_PORT = 10002
FLASH_SERVER_HOST = "127.0.0.1"
PAGE_SIZE = 4000

class TestEndToEnd(unittest.TestCase):
    """Tests flash service functionality."""

    @classmethod
    def setUpClass(cls):
        # start sequencer
        cls.sequencer_thread = test.helper.ServerThread(SEQUENCER_PORT,
            SEQUENCER_HOST, get_token_service.GetTokenImpl())
        cls.sequencer_thread.start_server()
        cls.sequencer_service = RpcService(get_token_pb2.GetTokenService_Stub,
            SEQUENCER_PORT, SEQUENCER_HOST)

        # start flash server
        cls.flash_server_thread = test.helper.ServerThread(FLASH_SERVER_PORT,
            FLASH_SERVER_HOST, flash_service.FlashServiceImpl())
        cls.flash_server_thread.start_server()
        cls.flash_service = RpcService(flash_service_pb2.FlashService_Stub,
            FLASH_SERVER_PORT, FLASH_SERVER_HOST)
        cls._reset_flash_server()

    @classmethod
    def tearDownClass(cls):
        cls._reset_flash_server()

    @classmethod
    def _reset_flash_server(cls):
        reset_request = flash_service_pb2.ResetRequest()
        reset_response = TestEndToEnd.flash_service.Reset(reset_request)
        assert(reset_response.status == flash_service_pb2.ResetResponse.SUCCESS)

    def test_append(self):
        pass

    def test_read(self):
        pass

if __name__ == "__main__":
    unittest.main()


