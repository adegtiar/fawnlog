SEQUENCER_HOST = "54.201.84.70"
SEQUENCER_PORT = 10001

SERVER_ADDR_LIST = [("127.0.0.1", 10002),
                    ("127.0.0.1", 10003),
                    ("127.0.0.1", 10004),
                    ("127.0.0.1", 10005),
                    ("127.0.0.1", 10006),
                    ("127.0.0.1", 10007),
                    ("127.0.0.1", 10008)]

FLASH_FILE_PATH = "pagefile.flog"
FLASH_PAGE_NUMBER = 40000
DEFAULT_BLOCK_SIZE = 2048
FLASH_PAGE_SIZE = DEFAULT_BLOCK_SIZE - 4 # Includes header size.
FLASH_PER_GROUP = 3 # number of servers per group
