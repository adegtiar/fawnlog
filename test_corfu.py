from fawnlog import config
from fawnlog import client
from test import helper
from fawnlog import get_token_service
from fawnlog import flash_service

import sys
import random
import threading


latencies = []


def _start_sequencer():
    sequencer_thread = helper.ServerThread(config.SEQUENCER_PORT,config.SEQUENCER_HOST, get_token_service.GetTokenImpl())
    sequencer_thread.start_server()

def _start_flash_servers():
    server_index = 0
    for (host, port) in config.SERVER_ADDR_LIST:
        server_thread = helper.ServerThread(port, host,
        flash_service.FlashServiceImpl(server_index))
        server_index += 1
        server_thread.start_server()

def _client_impl(number_of_pages):
    c = client.Client()
    latency_list = []
    for _ in xrange(number_of_pages):
        data_str_list = []
        for _ in xrange(config.FLASH_PAGE_SIZE):
            data_str_list.append(chr(random.randint(65, 90)))
        data_str = ''.join(data_str_list)
        (_, ll) = c.append(data_str)
        latency_list.extend(ll)
    latencies.append(sum(latency_list) / number_of_pages)

def _start_clients(number_of_clients, number_of_pages):
    threads = []
    for _ in xrange(number_of_clients):
        threads.append(threading.Thread(target=_client_impl, args=(number_of_pages, )))
    for i in xrange(number_of_clients):
        threads[i].start()
    for i in xrange(number_of_clients):
        threads[i].join()
    result = sum(latencies) / number_of_clients
    print "the average latency of writing a page is {0} seconds".format(result)


class TestCorfu(object):
    ''' Given the number of clients, the number of pages written by each
        client, and then output the average latency in seconds.
    '''

    def __init__(self, number_of_clients, number_of_pages):
        self.number_of_clients = number_of_clients
        self.number_of_pages = number_of_pages
        self.average_latency = 0.0

    def run(self):
        _start_sequencer()
        _start_flash_servers()
        _start_clients(number_of_clients, number_of_pages)


if __name__ == "__main__":
    number_of_clients = int(sys.argv[1])
    number_of_pages = int(sys.argv[2])
    test_corfu = TestCorfu(number_of_clients, number_of_pages)
    test_corfu.run()
