"""Helper classes used for testing"""

import protobuf.socketrpc.server
import threading

class ServerThread(threading.Thread):
    """Starts server in a seperate thread for testing"""

    def __init__(self, port, host, service):
        """param: service: RPC service implementation"""

        threading.Thread.__init__(self)

        self.service = service
        self.server = protobuf.socketrpc.server.SocketRpcServer(port, host)
        self.server.registerService(self.service)
        self.setDaemon(True)

    def run(self):
        self.server.run()

    def reset(self, *args, **kwargs):
        self.service.reset(*args, **kwargs)

