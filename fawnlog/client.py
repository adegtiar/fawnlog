from fawnlog import config
from fawnlog import projection
from fawnlog import client_to_seq_pb2
from fawnlog import flash_service_pb2
from protobuf.socketrpc import RpcService
from uuid import uuid4

import threading
import time


class Client(object):
    ''' Client handles the write and read requests to the shared log.
        It communicates with the sequencer and server using protobuf.

    '''
    def __init__(self):
        self.projection = projection.Projection()
        self.service = RpcService(client_to_seq_pb2.GetTokenService_Stub,
                                  config.SEQUENCER_PORT,
                                  config.SEQUENCER_HOST)
        self.client_id = str(uuid4())
        # guessing information
        self.last_token = -2
        self.last_server = -1
        self.last_timestamp = 0.0
        self.last_ips = 0.0

    def append(self, data):
        ''' string -> int list

            Checking length of data and for every piece of the data, try
            guessing a server to write to and waiting for response. If a
            guess failed, retry writing. Every time some feedback helps to
            guess better next time. Return the list of tokens storing the data.

            Failure Handling:
                Sequencer returns specific token ID when the guessing server
                is already full.

            Exception Handling:
                NONE

        '''
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
                threading.Thread(target=self.send_to_sequencer,
                                 args=(server_w, piece_id)).start()
                response_w = self.write_to_flash(server_w,
                                                 piece_data,
                                                 piece_id)
                if response_w.status == flash_service_pb2.WriteResponse.SUCCESS:
                    token_list.append(response_w.token)
                    self.last_token = response_w.token
                    self.last_server = server_w
                    self.last_timestamp = response_w.timestamp
                    self.last_ips = response_w.ips
                    break
                else:
                    self.last_token = -1
                    self.last_server = server_w
                    self.last_timestamp = 0.0
                    self.last_ips = 0.0

        return token_list

    def guess_server(self):
        ''' None -> int

            Guess the next server that should be written to.

        '''
        if self.last_token == -2:
            # the client write for the first time
            return 0
        elif self.last_token == -1:
            # the server contacted last time is full
            return self.last_server + 1
        else:
            guess_inc = int((time.time() - self.last_timestamp) * self.last_ips)
            guess_token = self.last_token + guess_inc
            (_, guess_host, _, _) = self.projection.translate(guess_token)
            return guess_host

    def send_to_sequencer(self, flash_unit_number, data_id):
        ''' int * int -> GetTokenResponse

            Send server and data id to the sequencer, ignores the response.

        '''
        request_seq = client_to_seq_pb2.GetTokenRequest()
        request_seq.flash_unit_number = flash_unit_number
        request_seq.data_id = data_id
        response_seq = self.service.Write(request_seq, timeout=10000)
        return response_seq

    def write_to_flash(self, server, data, data_id):
        ''' int * string * int -> WriteResponse.Status

            Send data and its id to the server, and wait until the response
            is back.

            Failure Handling:
                NONE

            Exception Handling:
                NONE

        '''
        # data must be fit in a page right now
        (dest_host, dest_port) = config.SERVER_ADDR_LIST[server]
        service_w = RpcService(flash_service_pb2.FlashService_Stub,
                               dest_port, dest_host)
        request_w = flash_service_pb2.WriteRequest()
        request_w.data = data
        request_w.data_id = data_id
        response_w = service_w.Write(request_w, timeout=10000)
        return response_w

    def read(self, token):
        ''' int -> string

            Read the data stored in the given token of the shared log.

            Failure Handling:
                Raise an exception up to the client.

            Exception Handling:
                NONE

        '''
        (_, dest_host, dest_port, dest_page) = self.projection.translate(token)
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
