SEQUENCER_HOST = "54.200.180.127"
SEQUENCER_PORT = 10001

COUNT_IPS_INTERVAL = 0.1 # seconds
COUNT_IPS_ALPHA = 0.5 # weight for exponential moving average calculation
REQUEST_TIMEOUT = 0.1 # seconds

SERVER_ADDR_LIST = [("54.201.158.32", 10002),
                    ("54.201.7.112", 10002),
                    ("54.201.72.55", 10002),
                    ("54.200.85.65", 10002),
                    ("127.0.0.1", 10002),
                    ("127.0.0.1", 10002),
                    ("127.0.0.1", 10002),
                    ("127.0.0.1", 10002)]

FLASH_FILE_PATH = "pagefile.flog"
# The time interval (in seconds) since a flash unit receives an offset
# after which an unwritten page is considered a hole.
FLASH_HOLE_DELAY_THRESHOLD = 1.0
FLASH_PAGE_NUMBER = 40000
DEFAULT_BLOCK_SIZE = 4096
FLASH_PAGE_SIZE = DEFAULT_BLOCK_SIZE - 4 # Includes header size.
FLASH_PER_GROUP = 2 # number of servers per group
