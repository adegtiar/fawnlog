import collections
import os.path
import threading

from fawnlog import config
from fawnlog import flashlib


class TokenBuffer(object):
    """A synchronized table of token buffers."""

    def __init__(self):
        self.buffer_table = collections.defaultdict(TokenBuffer.BufferEntry)
        self.buffer_lock = threading.Lock()

    def pop_token_message(self, data_id):
        """Retrieves and removes the token message for the given data_id.

        This call blocks until the token is added to the buffer.

        """
        with self.buffer_lock:
            entry = self.buffer_table[data_id]
        entry.token_indicator.acquire()
        del self.buffer_table[data_id]
        return entry.token_message

    def put_token_message(self, data_id, token_message):
        """Adds a token message to the buffer."""
        with self.buffer_lock:
            entry = self.buffer_table[data_id]
        entry.token_message = token_message
        entry.token_indicator.release()

    class BufferEntry(object):
        def __init__(self):
            self.token_indicator = threading.Semaphore(0)
            self.token_message = None


class FlashUnit(object):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self, server_index):
        filepath = FlashUnit._get_filepath(server_index)
        self.pagestore = flashlib.PageStore(filepath, config.FLASH_PAGE_SIZE,
                config.FLASH_PAGE_NUMBER)
        self.token_buffer = TokenBuffer()

    def read(self, offset):
        return self.pagestore.read(offset)

    def write(self, data_id, data):
        token_message = self.token_buffer.pop_token_message(data_id)
        if token_message.is_full:
            raise flashlib.ErrorNoCapacity()
        else:
            self.page_store.write(token_message.offset, data)
            return token_message.measure

    def write_offset(self, data_id, offset_message):
        self.token_buffer.put_token_mssage(data_id, token_message)

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
