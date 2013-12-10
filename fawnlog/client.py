from fawnlog import config as global_config
from fawnlog import projection
from fawnlog import sequencer_service_pb2
from fawnlog import flash_service_pb2
from fawnlog import utils
from protobuf.socketrpc import RpcService
from uuid import uuid4

import math
import time
import random


INITIAL, SUCCESS, FULL, FAIL = range(4)


class Callback:
    def run(self, response):
        pass


class Client(object):
    ''' Client handles the write and read requests to the shared log.
        It communicates with the sequencer and server using protobuf.

    '''
    def __init__(self, config=global_config):
        self.projection = projection.Projection(config)
        self.service = RpcService(sequencer_service_pb2.SequencerService_Stub,
                                  config.SEQUENCER_PORT,
                                  config.SEQUENCER_HOST)
        self.client_id = str(uuid4())
        # guessing information
        self.largest_token = -1
        self.largest_timestamp = 0.0
        self.last_state = INITIAL
        self.last_server = -1
        self.latest_ips = 0.0
        self.delay = 0.0
        self.config = config

    def append(self, data):
        ''' string -> (int list * float list)

            Checking length of data and for every piece of the data, try
            guessing a server to write to and waiting for response. If a
            guess fails, retry writing. Every time some feedback helps to
            guess better next time. Return the list of tokens storing the
            data.

            Failure Handling:
                Sequencer returns specific token ID when the guessing server
                is already full.

            Exception Handling:
                NONE

        '''
        data_len = len(data)
        if data_len == 0:
            return []

        number_of_tokens = (data_len - 1) // self.config.FLASH_PAGE_SIZE + 1
        token_list = []

        # try send every piece of data by guessing
        for i in xrange(number_of_tokens):
            piece_beg = i * self.config.FLASH_PAGE_SIZE
            piece_end = (i + 1) * self.config.FLASH_PAGE_SIZE
            if i == number_of_tokens - 1:
                piece_end = data_len
            piece_data = data[piece_beg:piece_end]

            while True:
                server_w = self.guess_server()
                piece_id = self.client_id
                self.send_to_sequencer(server_w, piece_id)
                request_timestamp = utils.nanotime()
                start_time = time.time()
                response_w = self.write_to_flash(server_w, piece_data, piece_id)
                end_time = time.time()
                self.update_guess_info(response_w, request_timestamp, server_w)
                if response_w.status == flash_service_pb2.WriteResponse.SUCCESS:
                    token_list.append(response_w.measure.token)
                    break

        return token_list

    def update_guess_info(self, response, request_timestamp, server):
        ''' update information about guessing after the response from flash
        '''
        ips_measure = response.measure
        if response.status == flash_service_pb2.WriteResponse.SUCCESS:
            if self.largest_token < ips_measure.token:
                self.largest_token = ips_measure.token
                self.largest_timestamp = ips_measure.token_timestamp
            self.latest_ips = ips_measure.ips
            self.delay = ips_measure.request_timestamp - request_timestamp
            assert(self.delay >= 0)
            self.last_state = SUCCESS
        elif response.status == flash_service_pb2.WriteResponse.ERROR_NO_CAPACITY:
            self.latest_ips = ips_measure.ips
            self.last_server = server
            self.last_state = FULL
        else:
            self.latest_ips = ips_measure.ips
            self.last_state = FAIL

    def guess_server(self):
        ''' None -> int

            Guess the next server that should be written to.

        '''
        if self.last_state == INITIAL:
            return 0
        elif self.last_state == FULL:
            return self.last_server + 1
        else:
            # SUCCESS or FAIL here
            guess_inc = (utils.nanos_to_sec(self.delay + utils.nanotime() -
                self.largest_timestamp) * self.latest_ips + 1 +
                self.config.CLIENT_GUESS_OVERESTIMATION)
            guess_token = int(math.ceil(self.largest_token + guess_inc))
            guess_token += random.randint(1, 2)
            (guess_server, _, _, _) = self.projection.translate(guess_token)
            return guess_server


    def send_to_sequencer(self, flash_unit_number, data_id):
        ''' int * int -> SequencerServiceResponse

            Asyncronously send server and data id to the sequencer, ignores
            the response.

        '''
        request_seq = sequencer_service_pb2.SequencerServiceRequest()
        request_seq.flash_unit_number = flash_unit_number
        request_seq.data_id = data_id
        response_seq = self.service.Write(request_seq,
                                          timeout=10000,
                                          callback=Callback())
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
        (dest_host, dest_port) = self.config.SERVER_ADDR_LIST[server]
        service_w = RpcService(flash_service_pb2.FlashService_Stub,
                               dest_port, dest_host)
        request_w = flash_service_pb2.WriteRequest()
        request_w.data_id = data_id
        request_w.data = data
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

    def reset_guess_info(self):
        self.largest_token = -1
        self.largest_timestamp = 0.0
        self.last_state = INITIAL
        self.last_server = -1
        self.latest_ips = 0.0
        self.delay = 0.0

    def trim(self, token):
        # we don't need trim in this project
        pass

    def fill(self, token):
        # holes will be filled by servers
        pass
