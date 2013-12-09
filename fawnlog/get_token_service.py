#!/usr/bin/env python2.7
"""
   GetToken RPC server implementation.
"""

import config
import get_token_pb2
import logging
import protobuf.socketrpc.server
import sequencer

class GetTokenImpl(get_token_pb2.GetTokenService):
    """GetToken service implementation."""

    def __init__(self, logger=None):
        self.sequencer = sequencer.Sequencer()
        self.logger = logger or logging.getLogger(__name__)

    def GetToken(self, controller, request, done):
        number = request.number
        self.logger.debug("request number: {0}".format(number))

        response = get_token_pb2.GetTokenResponse()
        response.token = self.sequencer.get_token(number)
        self.logger.debug("response token: {0}".format(response.token))

        done.run(response)

    def reset(self, counter):
        """Reset sequencer counter, convenience function for testing"""
        self.sequencer.reset(counter)

def start_server():
    logger = logging.getLogger(__name__)
    logger.info("Starting sequencer server on port {0}:{1}".format(
        config.SEQUENCER_HOST, config.SEQUENCER_PORT))
    server = protobuf.socketrpc.server.SocketRpcServer(config.SEQUENCER_PORT)
    server.registerService(GetTokenImpl(logger))
    server.run()

if __name__ == '__main__':
    protobuf_log = logging.getLogger("protobuf.socketrpc.server")
    protobuf_log.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    start_server()
