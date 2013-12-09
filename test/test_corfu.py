import sys


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

    def _start_sequencer():
        sequencer_thread = test.helper.ServerThread(config.SEQUENCER_PORT,
                    config.SEQUENCER_HOST, get_token_service.GetTokenImpl())
        sequencer_thread.start_server()

    def _start_flash_servers():



if __name__ == "__main__":
    number_of_clients = int(sys.arg[0])
    number_of_pages = int(sys.arg[1])
    test_corfu = TestCorfu(number_of_clients, number_of_pages)
    test_corfu.run()
