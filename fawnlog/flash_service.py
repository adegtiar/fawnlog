#!/usr/bin/env python2.7
"""The fawnlog server backend, which hosts an individual flash unit."""

import logging
import sys

import protobuf.socketrpc.server

from fawnlog import config as global_config
from fawnlog import flashlib
from fawnlog import flash_service_pb2

from fawnlog.flash_unit import FlashUnit


class FlashServiceImpl(flash_service_pb2.FlashService):
    """Handles RPC requests to read and write pages on flash storage."""

    def __init__(self, flash_unit, logger=None):
        self.flash_unit = flash_unit
        self.logger = logger or logging.getLogger(__name__)

    @classmethod
    def from_index(cls, server_index=0, config=global_config, logger=None):
        flash_unit = FlashUnit(server_index, config)
        return FlashServiceImpl(flash_unit, logger)

    def Read(self, controller, request, done):
        """Reads the data from the page at the given offset."""
        self.logger.debug("Received read request: {0}".format(request))
        response = flash_service_pb2.ReadResponse()

        try:
            data = self.flash_unit.read(request.offset)
        except flashlib.ErrorUnwritten:
            status = flash_service_pb2.ReadResponse.ERROR_UNWRITTEN
        except flashlib.ErrorFilledHole:
            status = flash_service_pb2.ReadResponse.ERROR_FILLED_HOLE
        else:
            response.data = data
            status = flash_service_pb2.ReadResponse.SUCCESS

        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def Write(self, controller, request, done):
        """Writes the given data, blocking until it receives a offset."""
        self.logger.debug("Received write request: {0}".format(request))
        response = flash_service_pb2.WriteResponse()

        try:
            ips_measure = self.flash_unit.write(request.data_id, request.data)
        except flashlib.ErrorOverwritten as err:
            status = flash_service_pb2.WriteResponse.ERROR_OVERWRITTEN
            ips_measure = err.ips_measure
        except flashlib.ErrorFilledHole as err:
            status = flash_service_pb2.WriteResponse.ERROR_FILLED_HOLE
            ips_measure = err.ips_measure
        except flashlib.ErrorNoCapacity as err:
            status = flash_service_pb2.WriteResponse.ERROR_NO_CAPACITY
            ips_measure = err.ips_measure
        except ValueError as err:
            status = flash_service_pb2.WriteResponse.ERROR_OVERSIZED_DATA
            ips_measure = err.ips_measure
        else:
            status = flash_service_pb2.WriteResponse.SUCCESS

        response.measure.CopyFrom(ips_measure)
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)

    def WriteOffset(self, controller, request, done):
        """Writes the given data to the page at the given offset."""
        self.logger.debug("Received WriteOffset request: {0}".format(request))

        self.flash_unit.write_offset(request.data_id, request)

        done.run(flash_service_pb2.WriteOffsetResponse())

    def FillHole(self, controller, request, done):
        """Fills a hole at the page at the given offset."""
        self.logger.debug("Received fill_hole request: {0}".format(request))
        response = flash_service_pb2.FillHoleResponse()

        try:
            self.flash_unit.fill_hole(request.offset)
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
            self.flash_unit.reset()
        except OSError:
            status = flash_service_pb2.ResetResponse.ERROR
        else:
            status = flash_service_pb2.ResetResponse.SUCCESS
        response.status = status
        self.logger.debug("Responding with response: {0}".format(response))

        done.run(response)


def main(server_index):
    logger = logging.getLogger(__name__)
    host, port = global_config.SERVER_ADDR_LIST[server_index]

    # Start the server.
    logger.info("Starting flash server {0} on {1}:{2}".format(server_index,
        host, port))
    server = protobuf.socketrpc.server.SocketRpcServer(port, "0.0.0.0")

    try:
        with FlashUnit(server_index, global_config) as flash_unit:
            server.registerService(FlashServiceImpl(flash_unit))
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
