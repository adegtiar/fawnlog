import collections
import os.path
import threading

from fawnlog import config
from fawnlog import flashlib


class OffsetBuffer(object):
    """A synchronized table of offset buffers."""

    def __init__(self):
        self.buffer_table = collections.defaultdict(OffsetBuffer.BufferEntry)
        self.buffer_lock = threading.Lock()

    def pop_offset_message(self, data_id):
        """Retrieves and removes the offset message for the given data_id.

        This call blocks until the offset is added to the buffer.

        """
        with self.buffer_lock:
            entry = self.buffer_table[data_id]
        entry.offset_indicator.acquire()
        del self.buffer_table[data_id]
        return entry.offset_message

    def put_offset_message(self, data_id, offset_message):
        """Adds a offset message to the buffer."""
        with self.buffer_lock:
            entry = self.buffer_table[data_id]
        entry.offset_message = offset_message
        entry.offset_indicator.release()

    class BufferEntry(object):
        def __init__(self):
            self.offset_indicator = threading.Semaphore(0)
            self.offset_message = None


class FlashUnit(object):
    """Handles requests to read and write pages on flash storage."""

    def __init__(self, server_index):
        filepath = FlashUnit._get_filepath(server_index)
        self.pagestore = flashlib.PageStore(filepath, config.FLASH_PAGE_SIZE,
                config.FLASH_PAGE_NUMBER)
        self.offset_buffer = OffsetBuffer()

    def read(self, offset):
        return self.pagestore.read(offset)

    def write(self, data_id, data):
        offset_message = self.offset_buffer.pop_offset_message(data_id)
        if offset_message.is_full:
            raise flashlib.ErrorNoCapacity()
        else:
            self.page_store.write(offset_message.offset, data)
            return offset_message.measure

    def write_offset(self, data_id, offset_message):
        self.offset_buffer.put_offset_mssage(data_id, offset_message)

    def fill_hole(self, offset):
        self.pagestore.fill_hole(offset)

    def reset(self):
        self.pagestore.reset()
        self.offset_buffer = OffsetBuffer()

    def close(self):
        self.pagestore.close()

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        self.close()

    @staticmethod
    def _get_filepath(server_index):
        base_path, ext = os.path.splitext(config.FLASH_FILE_PATH)
        return "{0}_{1}{2}".format(base_path, server_index, ext)
