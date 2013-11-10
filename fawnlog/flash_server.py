"""The fawnlog server backend, which hosts an individual flash unit."""


from fawnlog import config
from fawnlog import flashlib


class FlashServer(object):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self):
        self.pagestore = PageStore(config.FLASH_FILE_PATH,
                                   config.FLASH_PAGE_SIZE)

    def read(self, page_index):
        """Reads the data from the page at the given offset."""
        return self.pagestore.read(page_index)

    def write(self, data, page_index):
        """Writes the given data to the page at the given offset."""
        self.pagestore.write(page_index)
