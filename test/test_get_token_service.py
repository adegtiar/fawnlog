#!/usr/bin/env python2.7
"""Tests get token service."""

import unittest
import helper

from fawnlog import get_token_pb2
from fawnlog import get_token_service
from protobuf.socketrpc import RpcService

SEQUENCER_HOST = "127.0.0.1"
SEQUENCER_PORT = 9999

class TestGetTokenService(unittest.TestCase):
    """Tests get token service functionality."""

    @classmethod
    def setUpClass(cls):
        # start server thread
        cls.server_thread = helper.ServerThread(SEQUENCER_PORT,
            SEQUENCER_HOST, get_token_service.GetTokenImpl())
        cls.server_thread.start_server()
        cls.service = RpcService(get_token_pb2.GetTokenService_Stub,
            SEQUENCER_PORT, SEQUENCER_HOST)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_token_basic(self):
        token = 10
        TestGetTokenService.server_thread.reset(token)
        request = get_token_pb2.GetTokenRequest()
        request.number = 1
        response = TestGetTokenService.service.GetToken(request, timeout=10000)
        self.assertEqual(response.token, token)

    def test_get_token_multiple(self):
        token = 10
        TestGetTokenService.server_thread.reset(token)
        for i in range(100, 10000, 100):
            request = get_token_pb2.GetTokenRequest()
            request.number = i
            response = TestGetTokenService.service.GetToken(
                request, timeout=10000)
            self.assertEqual(response.token, token)
            token += i
        
if __name__ == "__main__":
    unittest.main()
