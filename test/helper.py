"""Helper classes used for testing"""

import protobuf.socketrpc.server
import threading

class ServerThread(threading.Thread):
    instance = None

    def __init__(self, port, host, service):
        """param: service: RPC service implementation"""

        threading.Thread.__init__(self)

        self.service = service
        self.server = protobuf.socketrpc.server.SocketRpcServer(port, host)
        self.server.registerService(self.service)
        self.setDaemon(True)
    
    @classmethod
    def start_server(cls, port, host, service):
        if cls.instance == None:
            cls.instance = ServerThread(port, host, service)
            cls.instance.start()

    @classmethod
    def reset(cls, *args, **kwargs):
        if cls.instance != None:
            cls.instance.service.reset(*args, **kwargs)

    def run(self):
        self.server.run()
