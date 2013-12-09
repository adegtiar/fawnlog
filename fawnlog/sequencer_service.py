#!/usr/bin/env python2.7
"""
   Sequencer RPC server implementation.
"""

from fawnlog import config
from fawnlog import sequencer_service_pb2
from fawnlog import sequencer
import logging
import protobuf.socketrpc.server

class SequencerServiceImpl(sequencer_service_pb2.SequencerService):
    """Sequencer service implementation."""

    def __init__(self, logger=None):
        self.sequencer = sequencer.Sequencer()
        self.logger = logger or logging.getLogger(__name__)

    def Write(self, controller, request, done):
        flash_unit_number = request.flash_unit_number
        data_id = request.data_id
        self.logger.debug("client write to server {0} data_id {1}".format(
            flash_unit_number, data_id))

        response = sequencer_service_pb2.SequencerServiceResponse()
        self.sequencer.insert_request(data_id, flash_unit_number)
        done.run(response)

    def reset(self, token):
        """Reset sequencer token, convenience function for testing"""
        self.sequencer.reset(token)

def start_server():
    logger = logging.getLogger(__name__)
    logger.info("Starting sequencer server on port {0}:{1}".format(
        config.SEQUENCER_HOST, config.SEQUENCER_PORT))
    server = protobuf.socketrpc.server.SocketRpcServer(
        config.SEQUENCER_PORT, config.SEQUENCER_HOST)
    server.registerService(SequencerServiceImpl(logger))
    server.run()

if __name__ == '__main__':
    protobuf_log = logging.getLogger("protobuf.socketrpc.server")
    protobuf_log.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    start_server()
