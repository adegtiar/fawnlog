SEQUENCER_HOST = "54.201.87.120"
SEQUENCER_PORT = 10001

SERVER_ADDR_LIST = [("54.201.143.215", 10002),
                    ("54.201.140.226", 10002),
                    ("54.201.136.144", 10002),
                    ("54.201.139.2", 10002),
                    ("54.201.142.124", 10002),
                    ("54.201.117.166", 10002),
                    ("127.0.0.1", 10002)]


FLASH_FILE_PATH = "pagefile.flog"
FLASH_PAGE_NUMBER = 40000
DEFAULT_BLOCK_SIZE = 2048
FLASH_PAGE_SIZE = DEFAULT_BLOCK_SIZE - 4 # Includes header size.
FLASH_PER_GROUP = 2 # number of servers per group
