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

    def __init__(self, server_index=0, logger=None):
        filepath = FlashServiceImpl._get_filepath(server_index)
        self.pagestore = flashlib.PageStore(filepath, config.FLASH_PAGE_SIZE,
                config.FLASH_PAGE_NUMBER)
        self.logger = logger or logging.getLogger(__name__)

    def Read(self, controller, request, done):
        """Reads the data from the page at the given offset."""
        self.logger.debug("Received read request: {0}".format(request))
        response = flash_service_pb2.ReadResponse()

        data = None
        try:
            data = self.pagestore.read(request.offset)
        except flashlib.ErrorUnwritten:
            status, data = self._handle_read_unwritten(request.offset)
        except flashlib.ErrorFilledHole:
            status = flash_service_pb2.ReadResponse.ERROR_FILLED_HOLE
        else:
            status = flash_service_pb2.ReadResponse.SUCCESS

        response.status = status
        if data:
            response.data = data
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def _handle_read_unwritten(self, offset):
        """Handles the error of a read requests for an unwritten page.

        Checks if the page is likely to be a hole, and potentially fills it.

        """
        data = None
        if self._check_is_hole(offset):
            try:
                self.pagestore.fill_hole(offset)
            except ErrorOverwritten:
                # Unwritten page got written during check.
                status = flash_service_pb2.ReadResponse.SUCCESS
                data = self.pagestore.read(offset)
            else:
                # Page is now filled with a hole
                status = flash_service_pb2.ReadResponse.ERROR_FILLED_HOLE
        else:
            # This page is not a hole - simply not yet written.
            status = flash_service_pb2.ReadResponse.ERROR_UNWRITTEN

        return status, data

    def _check_is_hole(self, page):
        """Determines whether the page is likely to be a hole."""
        # TODO: implement this.
        return False

    def Write(self, controller, request, done):
        """Writes the given data to the page at the given offset."""
        self.logger.debug("Received write request: {0}".format(request))
        response = flash_service_pb2.WriteResponse()

        try:
            self.pagestore.write(request.data, request.offset)
        except flashlib.ErrorOverwritten:
            status = flash_service_pb2.WriteResponse.ERROR_OVERWRITTEN
        except flashlib.ErrorFilledHole:
            status = flash_service_pb2.WriteResponse.ERROR_FILLED_HOLE
        except ValueError:
            status = flash_service_pb2.WriteResponse.ERROR_OVERSIZED_DATA
        else:
            status = flash_service_pb2.WriteResponse.SUCCESS
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def FillHole(self, controller, request, done):
        """Fills a hole at the page at the given offset."""
        self.logger.debug("Received fill_hole request: {0}".format(request))
        response = flash_service_pb2.FillHoleResponse()

        try:
            self.pagestore.fill_hole(request.offset)
        except flashlib.ErrorOverwritten:
            status = flash_service_pb2.FillHoleResponse.ERROR_OVERWRITTEN
        else:
            status = flash_service_pb2.FillHoleResponse.SUCCESS
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

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        # Make sure the pagestore is closed.
        self.pagestore.close()

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

    try:
        with FlashServiceImpl(server_index) as flash_service:
            server.registerService(flash_service)
            server.run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    protobuf_log = logging.getLogger("protobuf.socketrpc.server")
    protobuf_log.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) < 2:
        print("Usage: flash_service.py <server_index>")
        sys.exit(1)

    main(int(sys.argv[1]))
