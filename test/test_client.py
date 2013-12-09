#!/usr/bin/env python2.7
"""Test client unit functionality."""

import unittest

from fawnlog import client


class TestClient(unittest.TestCase):
    """Tests client functionality."""

    def setUp(self):
        self.client = client.Client()

    def test_guess_server_initial(self):
        self.client.reset_guess_info()
        server = self.client.guess_server()
        self.assertEqual(server, 0)

    def test_guess_server_fail(self):
        self.client.reset_guess_info()
        self.client.largest_token = 0
        self.client.last_state = client.FAIL
        server = self.client.guess_server()
        self.assertNotEqual(server, -1)

    def test_guess_server_full(self):
        self.client.reset_guess_info()
        self.client.last_state = client.FULL
        server = self.client.guess_server()
        self.assertEqual(server, 0)


if __name__ == "__main__":
    unittest.main()
