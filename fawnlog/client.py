from fawnlog import config
from fawnlog import projection
from fawnlog import get_token_pb2
from fawnlog import flash_service_pb2
from protobuf.socketrpc import RpcService

import time


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
        """ string -> int list

            Checking length of data and get appropriate number of tokens
            from the sequencer. Then use those tokens to write to the
            shared log. Return the list of tokens storing the data.

            Failure Handling:
                If a write operation fails with one token, get a new token
                from the sequencer and retry writing the piece of data.

            Exception Handling:
                NONE

        """
        data_len = len(data)
        if data_len == 0:
            return []

        number_of_tokens = (data_len - 1) // config.FLASH_PAGE_SIZE + 1
        token_head = self.get_tokens(number_of_tokens)
        token_list = [token_head + i for i in range(0, number_of_tokens)]
        latency_list = []

        # try send every piece of data
        for i in range(number_of_tokens):
            cur_token = token_list[i]
            piece_beg = i * config.FLASH_PAGE_SIZE
            piece_end = (i + 1) * config.FLASH_PAGE_SIZE
            if i == number_of_tokens - 1:
                piece_end = data_len
            piece_data = data[piece_beg:piece_end]

            while True:
                start_time = time.time()
                status_w = self.write_to(piece_data, cur_token)
                if status_w == flash_service_pb2.WriteResponse.SUCCESS:
                    latency_list.append(time.time() - start_time)
                    break
                else:
                    new_token = self.get_tokens(1)
                    token_list[i] = new_token
                    cur_token = new_token
        return (token_list, latency_list)

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

    def get_tokens(self, num_tokens):
        ''' int -> int

            Given the number of tokens wanted, return a token number tok_head,
            indicating that the range of [tok_head, tok_head + num_tokens) is
            given by the sequencer.

            Failure Handling:
                NONE

            Exception Handling:
                NONE

        '''
        request_s = get_token_pb2.GetTokenRequest()
        request_s.number = num_tokens
        response_s = self.service.GetToken(request_s, timeout=10000)
        return response_s.token
