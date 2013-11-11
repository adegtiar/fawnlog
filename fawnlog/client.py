import config
import projection
import get_token_pb2
from protobuf.socketrpc import RpcService


class Client(object):
    """ Client handles the write and read requests to the shared log.
        It communicates with the sequencer and server using protobuf.

    """
    def __init__(self):
        self.projection = projection.Projection()
        self.service = RpcService(get_token_pb2.GetTokenService_Stub,
                                  config.SEQUENCER_PORT,
                                  config.SEQUENCER_HOST)

    def append(self, data):
        """ Assume data is string right now.
            Checking the length of data and get appropriate number
              of position tokens from sequencer
            Every position token got from the sequencer is whithin
              the range of [0, 2^64 - 1]
        """
        self.check_data(data)
        number_of_tokens = len(data) // config.FLASH_PAGE_SIZE + 1
        token_list = self.get_tokens(number_of_tokens)

        i = 1
        for token in token_list:
            beg = (i - 1) * config.FLASH_PAGE_SIZE
            if i < number_of_tokens:
                # not the last one
                end = i * config.FLASH_PAGE_SIZE
                self.write_to(data[beg:end], token)
            else:
                # the last one
                self.write_to(data[beg:], token)
            i += 1
        return token_list

    def write_to(self, data, token):
        # data must be fit in a page right now
        self.check_position(token)
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        server_socket = socket.socket(socket.AF_INET)
        server_socket.connect((dest_host, dest_port))
        # todo: write data to server
        # error is handled in the server
        return True

    def read(self, token):
        # todo: read data from server
        self.check_position(token)
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        server_socket = socket.socket(socket.AF_INET)
        server_socket.connect((dest_host, dest_port))
        # todo: read data from server
        # error is handled in the server
        return True

    def trim(self, token):
        self.check_position(token)
        return True

    def fill(self, token):
        self.check_position(token)
        data = "".join(["1"] * config.FLASH_PAGE_SIZE)
        return self.write_to(data, token)

    def get_tokens(self, num_tokens):
        request = get_token_pb2.GetTokenRequest()
        request.number = num_tokens
        try:
            return service.GetToken(request, timeout=10000)
        except Exception, ex:
            print ex

    def check_position(self, token):
        if not (isinstance(token, int)):
            raise Exception("token is not int")
        if token < 0:
            raise Exception("token is smaller than 0")
        if token >= 2 ** 64:
            raise Exception("token is bigger than 2^64 - 1")

    def check_data(self, data):
        if not (isinstance(data, str)):
            raise Exception("data is not string")
