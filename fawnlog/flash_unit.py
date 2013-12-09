import os.path

from fawnlog import config
from fawnlog import flashlib

class FlashUnit(object):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self, server_index):
        filepath = FlashUnit._get_filepath(server_index)
        self.pagestore = flashlib.PageStore(filepath, config.FLASH_PAGE_SIZE,
                config.FLASH_PAGE_NUMBER)

    def read(self, offset):
        return self.pagestore.read(offset)

    def write(self, data, offset):
        self.pagestore.write(data, offset)

    def fill_hole(self, offset):
        self.pagestore.fill_hole(offset)

    def reset(self):
        self.pagestore.reset()

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        # Make sure the pagestore is closed.
        self.pagestore.close()

    @staticmethod
    def _get_filepath(server_index):
        base_path, ext = os.path.splitext(config.FLASH_FILE_PATH)
        return "{0}_{1}{2}".format(base_path, server_index, ext)
