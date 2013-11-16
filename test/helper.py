"""Helper classes used for testing"""

import protobuf.socketrpc.server
import threading
import time

class ServerThread(threading.Thread):
    """Starts server in a seperate thread for testing"""

    def __init__(self, port, host, service):
        """
        param: service: RPC service implementation
        """
        threading.Thread.__init__(self)

        self.service = service
        self.server = protobuf.socketrpc.server.SocketRpcServer(port, host)
        self.server.registerService(self.service)
        self.setDaemon(True)
        self.running = False

    def run(self):
        self.running = True
        self.server.run()

    def start_server(self):
        self.start()
        while not self.running:
            time.sleep(1)

    def reset(self, *args, **kwargs):
        self.service.reset(*args, **kwargs)

