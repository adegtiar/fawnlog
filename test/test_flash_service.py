#!/usr/bin/env python2.7
"""Tests flash service."""

import unittest
import os

from protobuf.socketrpc import RpcService

import test.helper

from fawnlog import flash_service_pb2
from fawnlog import flash_service


FLASH_SERVER_PORT = 40001
FLASH_SERVER_HOST = "127.0.0.1"
PAGE_SIZE = 4000

class TestFlashService(unittest.TestCase):
    """Tests flash service functionality."""

    @classmethod
    def setUpClass(cls):
        # start server thread
        cls.server_thread = test.helper.ServerThread(FLASH_SERVER_PORT,
            FLASH_SERVER_HOST, flash_service.FlashServiceImpl.from_index(0))
        cls.server_thread.start_server()
        cls.service = RpcService(flash_service_pb2.FlashService_Stub,
            FLASH_SERVER_PORT, FLASH_SERVER_HOST)
        cls._reset_flash_server()

    def tearDown(self):
        self.__class__._reset_flash_server()

    @classmethod
    def _reset_flash_server(cls):
        reset_request = flash_service_pb2.ResetRequest()
        reset_response = TestFlashService.service.Reset(reset_request)
        assert(reset_response.status == flash_service_pb2.ResetResponse.SUCCESS)

    def test_write_read_basic(self):
        offset = 0
        data = os.urandom(PAGE_SIZE)
        response_w = self._write(offset, data)
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.SUCCESS)

        response_r = self._read(offset)
        self.assertEqual(response_r.status,
            flash_service_pb2.ReadResponse.SUCCESS)
        self.assertEqual(response_r.data, data)

    def test_read_unwritten(self):
        offset = 5000
        response_r = self._read(offset)
        self.assertEqual(response_r.status,
            flash_service_pb2.ReadResponse.ERROR_UNWRITTEN)

    def test_write_overwritten(self):
        offset = 10000
        data = os.urandom(PAGE_SIZE)
        # write once
        self._write(offset, data)
        # write again
        response_w = self._write(offset, data)
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.ERROR_OVERWRITTEN)

    def test_oversized_data(self):
        offset = 15000
        data = os.urandom(PAGE_SIZE*2)
        response_w = self._write(offset, data)
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.ERROR_OVERSIZED_DATA)

    def test_read_hole(self):
        offset = 5000
        response_fh = self._fill_hole(offset)
        self.assertEqual(response_fh.status,
            flash_service_pb2.FillHoleResponse.SUCCESS)

        response_r = self._read(offset)
        self.assertEqual(response_r.status,
            flash_service_pb2.ReadResponse.ERROR_FILLED_HOLE)

    def test_write_hole(self):
        offset = 5000
        response_fh = self._fill_hole(offset)
        self.assertEqual(response_fh.status,
            flash_service_pb2.FillHoleResponse.SUCCESS)

        response_w = self._write(offset, os.urandom(PAGE_SIZE))
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.ERROR_FILLED_HOLE)

    def test_fill_hole_basic(self):
        offset = 5000
        response_fh = self._fill_hole(offset)
        self.assertEqual(response_fh.status,
            flash_service_pb2.FillHoleResponse.SUCCESS)

    def test_fill_hole_overwritten(self):
        offset=5000
        data = os.urandom(PAGE_SIZE)
        response_w = self._write(offset, data)
        self.assertEqual(response_w.status,
            flash_service_pb2.WriteResponse.SUCCESS)

        response_fh = self._fill_hole(offset)
        self.assertEqual(response_fh.status,
            flash_service_pb2.FillHoleResponse.ERROR_OVERWRITTEN)

    def _read(self, offset):
        request_r = flash_service_pb2.ReadRequest()
        request_r.offset = offset
        response_r = TestFlashService.service.Read(request_r, timeout=10000)
        return response_r

    def _write(self, offset, data):
        data_id = "foo"

        # Write the offset.
        request_wo = flash_service_pb2.WriteOffsetRequest()
        request_wo.data_id = data_id
        request_wo.offset = offset
        request_wo.is_full = False
        request_wo.measure.token = 1
        request_wo.measure.token_timestamp = 2
        request_wo.measure.request_timestamp = 3
        request_wo.measure.ips = 4
        TestFlashService.service.WriteOffset(request_wo, timeout=10000)

        request_w = flash_service_pb2.WriteRequest()
        request_w.data_id = data_id
        request_w.data = data
        response_w = TestFlashService.service.Write(request_w, timeout=10000)
        return response_w

    def _fill_hole(self, offset):
        request_fh = flash_service_pb2.FillHoleRequest()
        request_fh.offset = offset
        response_fh = TestFlashService.service.FillHole(request_fh, timeout=10000)
        return response_fh

if __name__ == "__main__":
    unittest.main()
