#!/usr/bin/env python2.7
"""
   GetToken RPC server implementation.
"""

import config
import get_token_pb2
import protobuf.socketrpc.server as server
import sequencer

class GetTokenImpl(get_token_pb2.GetTokenService):
    """GetToken service implementation."""

    def __init__(self):
        self.sequencer = sequencer.Sequencer()

    def GetToken(self, controller, request, done):
        print "request: %s" % request,

        number = request.number

        response = get_token_pb2.GetTokenResponse()
        response.token = self.sequencer.get_token(number)
        print "respone: %s" % response.token

        done.run(response)


if __name__ == '__main__':
    get_token_service = GetTokenImpl()
    server = server.SocketRpcServer(config.SEQUENCER_PORT)
    server.registerService(get_token_service)

    # Start the server.
    print "Start sequencer server on port %s" % config.SEQUENCER_PORT
    server.run()
