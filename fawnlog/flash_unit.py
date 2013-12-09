import collections
import os.path
import threading
import time

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
        # WriteOffset timestamps, used for hole detection.
        self.offset_timestamps = dict()

    def read(self, offset):
        """Reads the page at the offset from the underlying pagestore.

        If the given offset has been received from the sequencer but not
        yet written by the client, the offset may be considered a hole
        and filled.

        """
        try:
            return self.pagestore.read(offset)
        except flashlib.ErrorUnwritten as err:
            if self._is_likely_hole(offset):
                try:
                    self.pagestore.fill_hole(offset)
                except flashlib.ErrorOverwritten:
                    # Page got written between check and fill.
                    return self.pagestore.read(offset)
                else:
                    raise flashlib.ErrorFilledHole()
            else:
                raise err

    def _is_likely_hole(self, offset):
        """Checks whether this offset is likely a hole.

        An offset is considered a hole when it has been written by the
        sequencer and at least config.FLASH_HOLE_DELAY_THRESHOLD seconds
        have passed.

        """
        try:
            time_since_offset = time.time() - self.offset_timestamps[offset]
        except KeyError:
            # This offset has not been received from the sequencer.
            return False
        else:
            return time_since_offset > config.FLASH_HOLE_DELAY_THRESHOLD

    def write(self, data_id, data):
        """Writes the data, blocking until the offset is received."""
        offset_message = self.offset_buffer.pop_offset_message(data_id)
        try:
            if offset_message.is_full:
                raise flashlib.ErrorNoCapacity()
            else:
                try:
                    self.pagestore.write(data, offset_message.offset)
                    return offset_message.measure
                finally:
                    del self.offset_timestamps[offset_message.offset]
        except ValueError as err:
            # Pass the measure even when there's an error.
            err.ips_measure = offset_message.measure
            raise err

    def write_offset(self, data_id, offset_message):
        """Writes the offset message for the given data id."""
        if not offset_message.is_full:
            self.offset_timestamps[offset_message.offset] = time.time()
        self.offset_buffer.put_offset_message(data_id, offset_message)

    def fill_hole(self, offset):
        """Fills the page at the given offset with a hole."""
        self.pagestore.fill_hole(offset)

    def reset(self):
        """Clears all data for the pagestore."""
        self.pagestore.reset()
        self.offset_buffer = OffsetBuffer()
        self.offset_timestamps = dict()

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
