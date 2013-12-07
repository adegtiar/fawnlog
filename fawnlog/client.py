from fawnlog import config
from fawnlog import projection
from fawnlog import get_token_pb2
from fawnlog import flash_service_pb2
from protobuf.socketrpc import RpcService
from uuid import uuid4


class Client(object):
    """ Client handles the write and read requests to the shared log.
        It communicates with the sequencer and server using protobuf.

    """
    def __init__(self):
        self.projection = projection.Projection()
        self.service = RpcService(get_token_pb2.GetTokenService_Stub,
                                  config.SEQUENCER_PORT,
                                  config.SEQUENCER_HOST)
        # guess_info: last_token * last_timestamp
        self.guess_info = (-1, 0.0)
        self.client_id = str(uuid4())

    def append(self, data):
        """ string -> int list

            Checking length of data and for every piece of the data, try
            guessing a server to write to and waiting for response. If a
            guess failed, retry writing. Every time some feedback helps to
            guess better next time. Return the list of tokens storing the data.

            Failure Handling:
                Sequencer returns specific token ID when the guessing server
                is already full.

            Exception Handling:
                NONE

        """
        data_len = len(data)
        if data_len == 0:
            return []

        number_of_tokens = (data_len - 1) // config.FLASH_PAGE_SIZE + 1
        token_list = []

        # try send every piece of data by guessing
        for i in xrange(number_of_tokens):
            piece_beg = i * config.FLASH_PAGE_SIZE
            piece_end = (i + 1) * config.FLASH_PAGE_SIZE
            if i == number_of_tokens - 1:
                piece_end = data_len
            piece_data = data[piece_beg:piece_end]

            while True:
                server_w = self.guess_server()
                piece_id = self.client_id
                self.send_to_sequencer(server_w, piece_id)
                response_w = self.write_to_server(piece_data, piece_id)
                if response_w == flash_service_pb2.WriteResponse.SUCCESS:
                    token_list.append(response_w.token)
                    self.guess_info = response_w.guess_info
                    break
                else:
                    self.guess_info = response_w.guess_info

        return token_list

    def guess_server(self):
        ''' None -> int

            Guess the next server that should be written to.

        '''
        if last_timestamp == 0.0:
            # the server contact last time is full


    def write_to(self, data, token):
        ''' string * int -> WriteResponse.Status

            Write data to the position 'token' in the shared log. Return
            the status of the operation to caller, either SUCCESS or ERROR.

            Failure Handling:
                Pop failure case up to caller.

            Exception Handling:
                NONE

        '''
        # data must be fit in a page right now
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        service_w = RpcService(flash_service_pb2.FlashService_Stub,
                               dest_port, dest_host)
        request_w = flash_service_pb2.WriteRequest()
        request_w.offset = dest_page
        request_w.data = data
        response_w = service_w.Write(request_w, timeout=10000)
        return response_w.status

    def read(self, token):
        ''' int -> string

            Read the data stored in the given token of the shared log.

            Failure Handling:
                Raise an exception up to the client.

            Exception Handling:
                NONE

        '''
        (dest_host, dest_port, dest_page) = self.projection.translate(token)
        service_r = RpcService(flash_service_pb2.FlashService_Stub,
                               dest_port, dest_host)
        request_r = flash_service_pb2.ReadRequest()
        request_r.offset = dest_page
        response_r = service_r.Read(request_r, timeout=10000)
        if response_r.status == flash_service_pb2.ReadResponse.SUCCESS:
            return response_r.data
        else:
            raise Exception("server read error")

    def trim(self, token):
        # we don't need trim in this project
        pass

    def fill(self, token):
        # holes will be filled by servers
        pass

