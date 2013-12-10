from fawnlog import config
from fawnlog import client
from test import helper
from fawnlog import get_token_service
from fawnlog import flash_service

import sys
import random
import threading
import os
import time


latencies = []


def _client_impl(number_of_pages, client_number):
    c = client.Client(config)
    latency_list = []
    for i in xrange(number_of_pages):
        data_str = os.urandom(config.FLASH_PAGE_SIZE)
        print "client_{0} appends {1}th page".format(client_number, i)
        start_time = time.time()
        _ = c.append(data_str)
        end_time = time.time()
        latency_list.append(end_time - start_time)
    latencies.append(sum(latency_list) / number_of_pages)

def _start_clients(number_of_clients, number_of_pages):
    threads = []
    for i in xrange(number_of_clients):
        threads.append(threading.Thread(target=_client_impl, args=(number_of_pages, i)))
    for i in xrange(number_of_clients):
        threads[i].start()
    for i in xrange(number_of_clients):
        threads[i].join()
    result = sum(latencies) / number_of_clients
    print "the average latency of appending a page is {0} seconds".format(result)


class TestCorfu(object):
    ''' Given the number of clients, the number of pages written by each
        client, and then output the average latency in seconds.
    '''

    def __init__(self, number_of_clients, number_of_pages):
        self.number_of_clients = number_of_clients
        self.number_of_pages = number_of_pages
        self.average_latency = 0.0

    def run(self):
        _start_clients(number_of_clients, number_of_pages)


if __name__ == "__main__":
    number_of_clients = int(sys.argv[1])
    number_of_pages = int(sys.argv[2])
    test_corfu = TestCorfu(number_of_clients, number_of_pages)
    test_corfu.run()
