"""Helper classes used for testing"""

import protobuf.socketrpc.server
import socket
import threading
import time

class ServerThread(threading.Thread):
    """Starts server in a seperate thread for testing"""

    def __init__(self, port, host, service):
        """
        param: service: RPC service implementation
        """
        threading.Thread.__init__(self)

        self.port = port
        self.host = host
        self.service = service
        self.server = protobuf.socketrpc.server.SocketRpcServer(port, host)
        self.server.registerService(self.service)
        self.setDaemon(True)

    def run(self):
        self.server.run()

    def start_server(self):
        self.start()
        while True:
            try:
                socket.create_connection((self.host, self.port))
            except socket.error:
                continue
            else:
                return

    def reset(self, *args, **kwargs):
        self.service.reset(*args, **kwargs)

