#!/usr/bin/env python2.7
"""Tests flash service."""

import unittest
import helper
import os

from fawnlog import flash_service_pb2
from fawnlog import flash_service
from protobuf.socketrpc import RpcService

FLASH_SERVER_PORT = 40001
FLASH_SERVER_HOST = "127.0.0.1"
PAGE_SIZE = 1024

class TestFlashService(unittest.TestCase):
    """Tests flash service functionality."""

    def setUp(self):
        self.service_impl = flash_service.FlashServiceImpl()
        # start server thread
        helper.ServerThread.start_server(FLASH_SERVER_PORT,
            FLASH_SERVER_HOST, self.service_impl)
        self.service = RpcService(flash_service_pb2.FlashService_Stub,
            FLASH_SERVER_PORT, FLASH_SERVER_HOST)

    def tearDown(self):
        pass

    def test_write_read_basic(self):
        offset = 25
        data = os.urandom(PAGE_SIZE)
        request_w = flash_service_pb2.WriteRequest()
        request_w.offset = offset
        request_w.data = data
        response_w = self.service.Write(request_w, timeout=10000)
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.SUCCESS)

        request_r = flash_service_pb2.ReadRequest()
        request_r.offset = offset
        response_r = self.service.Read(request_r, timeout=10000)
        self.assertEqual(response_r.status,
            flash_service_pb2.ReadResponse.SUCCESS)
        self.assertEqual(response_r.data, data)

    def test_read_unwritten(self):
        pass

    def test_write_overwritten(self):
        pass

    def test_oversized_data(self):
        pass

if __name__ == "__main__":
    unittest.main()
