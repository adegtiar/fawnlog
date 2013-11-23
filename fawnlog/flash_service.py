#!/usr/bin/env python2.7
"""The fawnlog server backend, which hosts an individual flash unit."""

import logging
import os.path
import sys

import protobuf.socketrpc.server

from fawnlog import config
from fawnlog import flashlib
from fawnlog import flash_service_pb2


class FlashServiceImpl(flash_service_pb2.FlashService):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self, server_index, logger=None):
        filepath = FlashServiceImpl._get_filepath(server_index)
        self.pagestore = flashlib.PageStore(filepath, config.FLASH_PAGE_SIZE)
        self.logger = logger or logging.getLogger(__name__)

    def Read(self, controller, request, done):
        """Reads the data from the page at the given offset."""
        self.logger.debug("Received read request: {0}".format(request))
        response = flash_service_pb2.ReadResponse()

        try:
            data = self.pagestore.read(request.offset)
        except flashlib.ErrorUnwritten:
            status = flash_service_pb2.ReadResponse.ERROR_UNWRITTEN
        else:
            status = flash_service_pb2.ReadResponse.SUCCESS
            response.data = data
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def Write(self, controller, request, done):
        """Writes the given data to the page at the given offset."""
        self.logger.debug("Received read request: {0}".format(request))
        response = flash_service_pb2.WriteResponse()

        try:
            self.pagestore.write(request.data, request.offset)
        except flashlib.ErrorOverwritten:
            status = flash_service_pb2.WriteResponse.ERROR_OVERWRITTEN
        except ValueError:
            status = flash_service_pb2.WriteResponse.ERROR_OVERSIZED_DATA
        else:
            status = flash_service_pb2.WriteResponse.SUCCESS
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def Reset(self, controller, request, done):
        """Resets the server state, clearing all data."""
        self.logger.debug("Received reset request")
        response = flash_service_pb2.ResetResponse()

        try:
            self.pagestore.reset()
        except OSError:
            status = flash_service_pb2.ResetResponse.ERROR
        else:
            status = flash_service_pb2.ResetResponse.SUCCESS
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    @staticmethod
    def _get_filepath(server_index):
        base_path, ext = os.path.splitext(config.FLASH_FILE_PATH)
        return "{0}_{1}{2}".format(base_path, server_index, ext)


def main(server_index):
    logger = logging.getLogger(__name__)
    host, port = config.SERVER_ADDR_LIST[server_index]

    # Start the server.
    logger.info("Starting flash server {0} on {1}:{2}".format(server_index,
        host, port))
    server = protobuf.socketrpc.server.SocketRpcServer(port, host)
    server.registerService(FlashServiceImpl(server_index))
    server.run()


if __name__ == "__main__":
    protobuf_log = logging.getLogger("protobuf.socketrpc.server")
    protobuf_log.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print("Usage: flash_service.py <server_index>")
        sys.exit(1)

    main(int(sys.argv[1]))
