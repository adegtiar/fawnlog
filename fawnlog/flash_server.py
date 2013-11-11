#!/usr/bin/env python2.7
"""The fawnlog server backend, which hosts an individual flash unit."""

import sys
import threading

import protobuf.socketrpc.server

from fawnlog import config
from fawnlog import flashlib
from fawnlog import flash_service_pb2


class FlashServerThread(threading.Thread):
    """A background server thread with a registered flash service."""

    def __init__(self, port, host):
        threading.Thread.__init__(self)
        self.server = protobuf.socketrpc.server.SocketRpcServer(port, host)
        self.daemon = True

    def run(self):
        self.server.registerService(FlashServerImpl())
        self.server.run()


class FlashServerImpl(flash_service_pb2.FlashService):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self):
        self.pagestore = flashlib.PageStore(config.FLASH_FILE_PATH,
                config.FLASH_PAGE_SIZE)

    def Read(self, controller, request, done):
        """Reads the data from the page at the given offset."""
        print("Received read request: {0}".format(request))
        response = flash_service_pb2.ReadResponse()

        try:
            data = self.pagestore.read(request.offset)
        except flashlib.ErrorUnwritten:
            status = flash_service_pb2.ReadResponse.ERROR_UNWRITTEN
        else:
            status = flash_service_pb2.ReadResponse.SUCCESS
            response.data = data
        response.status = status
        print("Responding with response: {0}".format(response))

        done.run(response)

    def Write(self, controller, request, done):
        """Writes the given data to the page at the given offset."""
        print("Received read request: {0}".format(request))
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
        print("Responding with response: {0}".format(response))

        done.run(response)


def run_server(server_index):
    host, port = config.SERVER_ADDR_LIST[server_index]
    server_thread = FlashServerThread(port, host)

    # Start the server.
    print "Starting flash server on {0}:{1}".format(host, port)
    try:
        server_thread.run()
        server_thread.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: flash_server.py <server_index>"
        sys.exit(1)

    run_server(int(sys.argv[1]))
