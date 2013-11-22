#!/usr/bin/env python2.7
"""Tests flash service."""

import unittest

from protobuf.socketrpc import RpcService

import test.helper

import random

from fawnlog import client
from fawnlog import config
from fawnlog import get_token_pb2
from fawnlog import get_token_service
from fawnlog import flash_service_pb2
from fawnlog import flash_service


class TestEndToEnd(unittest.TestCase):
    """Tests flash service functionality."""

    @classmethod
    def setUpClass(cls):
        # start sequencer
        cls.sequencer_thread = test.helper.ServerThread(config.SEQUENCER_PORT,
            config.SEQUENCER_HOST, get_token_service.GetTokenImpl())
        cls.sequencer_thread.start_server()
        cls.sequencer_service = RpcService(get_token_pb2.GetTokenService_Stub,
            config.SEQUENCER_PORT, config.SEQUENCER_HOST)

        # start flash server 0
        (SERVER_0_HOST, SERVER_0_PORT) = config.SERVER_ADDR_LIST[0]
        cls.server_0_thread = test.helper.ServerThread(SERVER_0_PORT,
            SERVER_0_HOST, flash_service.FlashServiceImpl())
        cls.server_0_thread.start_server()
        cls.flash_service_0 = RpcService(flash_service_pb2.FlashService_Stub,
            SERVER_0_PORT, SERVER_0_HOST)

        # start flash server 1
        (SERVER_1_HOST, SERVER_1_PORT) = config.SERVER_ADDR_LIST[1]
        cls.server_1_thread = test.helper.ServerThread(SERVER_1_PORT,
            SERVER_1_HOST, flash_service.FlashServiceImpl())
        cls.server_1_thread.start_server()
        cls.flash_service_1 = RpcService(flash_service_pb2.FlashService_Stub,
            SERVER_1_PORT, SERVER_1_HOST)
        cls._reset_flash_server()

    @classmethod
    def tearDownClass(cls):
        cls._reset_flash_server()

    @classmethod
    def _reset_flash_server(cls):
        reset_request = flash_service_pb2.ResetRequest()
        reset_response_0 = TestEndToEnd.flash_service_0.Reset(reset_request)
        reset_response_1 = TestEndToEnd.flash_service_1.Reset(reset_request)
        assert(reset_response_0.status ==
                flash_service_pb2.ResetResponse.SUCCESS)
        assert(reset_response_1.status ==
                flash_service_pb2.ResetResponse.SUCCESS)

    def test_append_one_short(self):
        ''' test writing a short data to one page
        '''
        TestEndToEnd._reset_flash_server()

        test_str_list = []
        for _ in range(config.FLASH_PAGE_SIZE // 100):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        return_tokens = test_client.append(test_str)
        return_str = test_client.read(return_tokens[0])
        self.assertEqual(len(return_tokens), 1)
        self.assertEqual(test_str, return_str)

    def test_append_one_long(self):
        ''' test writing a long data to one page
        '''
        TestEndToEnd._reset_flash_server()

        test_str_list = []
        for _ in range(config.FLASH_PAGE_SIZE - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        return_tokens = test_client.append(test_str)
        return_str = test_client.read(return_tokens[0])
        self.assertEqual(len(return_tokens), 1)
        self.assertEqual(test_str, return_str)

    def test_append_two_page(self):
        ''' test writing to two pages
        '''
        TestEndToEnd._reset_flash_server()

        test_str_list = []
        for _ in range(config.FLASH_PAGE_SIZE * 2 - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        return_tokens = test_client.append(test_str)
        return_str_1 = test_client.read(return_tokens[0])
        return_str_2 = test_client.read(return_tokens[1])
        return_str = return_str_1 + return_str_2
        self.assertEqual(len(return_tokens), 2)
        self.assertEqual(test_str, return_str)

    def test_append_six_page(self):
        ''' test writing to nine pages
        '''
        TestEndToEnd._reset_flash_server()

        test_str_list = []
        for _ in range(config.FLASH_PAGE_SIZE * 9 - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        return_tokens = test_client.append(test_str)
        return_str = ""
        for token in return_tokens:
            return_str += test_client.read(token)
        self.assertEqual(len(return_tokens), 9)
        self.assertEqual(test_str, return_str)

if __name__ == "__main__":
    unittest.main()
