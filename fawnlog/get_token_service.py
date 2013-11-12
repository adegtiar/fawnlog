#!/usr/bin/env python2.7
"""
   GetToken RPC server implementation.
"""

import config
import get_token_pb2
import protobuf.socketrpc.server
import sequencer
import sys
import threading
import time

class GetTokenImpl(get_token_pb2.GetTokenService):
    """GetToken service implementation."""

    def __init__(self):
        self.sequencer = sequencer.Sequencer()

    def GetToken(self, controller, request, done):
        print("request: {0}".format(request))

        number = request.number

        response = get_token_pb2.GetTokenResponse()
        response.token = self.sequencer.get_token(number)
        print("respone: {0}".format(response.token))

        done.run(response)

    def reset(self, counter):
        """Reset sequencer counter, convenience function for testing"""
        self.sequencer.reset(counter)

def start_server():
    print("Start sequencer server on port {0}:{1}".format(
        config.SEQUENCER_HOST, config.SEQUENCER_PORT))
    server = protobuf.socketrpc.server.SocketRpcServer(
        config.SEQUENCER_PORT, config.SEQUENCER_HOST)
    server.registerService(GetTokenImpl())
    server.run()

if __name__ == '__main__':
    start_server()
