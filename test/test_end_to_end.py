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

SEQUENCER_PORT = 10001
SEQUENCER_HOST = "127.0.0.1"

SERVER_ADDR_LIST = [("127.0.0.1", 10002),
                    ("127.0.0.1", 10003),
                    ("127.0.0.1", 10004),
                    ("127.0.0.1", 10005),
                    ("127.0.0.1", 10006),
                    ("127.0.0.1", 10007),
                    ("127.0.0.1", 10008)]

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

        # start flash servers 0 and 1
        cls.flash_services = []
        for i in xrange(config.FLASH_PER_GROUP):
            cls.flash_services.append(cls._start_flash_server(i))

        cls._reset_flash_servers()

    @classmethod
    def tearDownClass(cls):
        cls._reset_flash_servers()

    @classmethod
    def _start_flash_server(cls, server_index):
        host, port = SERVER_ADDR_LIST[server_index]
        server_thread = test.helper.ServerThread(port, host,
                flash_service.FlashServiceImpl(server_index))
        server_thread.start_server()
        return RpcService(flash_service_pb2.FlashService_Stub, port, host)

    @classmethod
    def _reset_flash_servers(cls):
        for service in cls.flash_services:
            response = service.Reset(flash_service_pb2.ResetRequest())
            assert(response.status == flash_service_pb2.ResetResponse.SUCCESS)

    def test_append_one_short(self):
        ''' test writing a short data to one page
        '''
        TestEndToEnd._reset_flash_servers()

        test_str_list = []
        for _ in xrange(config.FLASH_PAGE_SIZE // 100):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        (return_tokens, _) = test_client.append(test_str)
        return_str = test_client.read(return_tokens[0])
        self.assertEqual(len(return_tokens), 1)
        self.assertEqual(test_str, return_str)

    def test_append_one_long(self):
        ''' test writing a long data to one page
        '''
        TestEndToEnd._reset_flash_servers()

        test_str_list = []
        for _ in xrange(config.FLASH_PAGE_SIZE - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        (return_tokens, _) = test_client.append(test_str)
        return_str = test_client.read(return_tokens[0])
        self.assertEqual(len(return_tokens), 1)
        self.assertEqual(test_str, return_str)

    def test_append_two_page(self):
        ''' test writing to two pages
        '''
        TestEndToEnd._reset_flash_servers()

        test_str_list = []
        for _ in xrange(config.FLASH_PAGE_SIZE * 2 - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        (return_tokens, _) = test_client.append(test_str)
        return_str_1 = test_client.read(return_tokens[0])
        return_str_2 = test_client.read(return_tokens[1])
        return_str = return_str_1 + return_str_2
        self.assertEqual(len(return_tokens), 2)
        self.assertEqual(test_str, return_str)

    def test_append_nine_page(self):
        ''' test writing to nine pages
        '''
        TestEndToEnd._reset_flash_servers()

        test_str_list = []
        for _ in xrange(config.FLASH_PAGE_SIZE * 9 - 1):
            test_str_list.append(chr(random.randint(65, 90)))
        test_str = ''.join(test_str_list)
        test_client = client.Client()
        (return_tokens, _) = test_client.append(test_str)
        return_str = ""
        for token in return_tokens:
            return_str += test_client.read(token)
        self.assertEqual(len(return_tokens), 9)
        self.assertEqual(test_str, return_str)

if __name__ == "__main__":
    unittest.main()
