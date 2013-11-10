"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""


import struct


class FlashStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to an infinite address range of pages. Writes must
    fit within a page. Enforces write-once semantics.

    """

    def __init__(self, filepath, page_size):
        total_page_size = page_size + len(FlashStore.get_header(page_size))
        self.datafile = PageFile(filepath, total_page_size)
        self.filepath = filepath

    def write_page(self, data, offset):
        """Writes the data to a page at the given offset."""
        page_entry_bytes = FlashStore.to_page_bytes(data)
        self.datafile.write(page_entry_bytes, offset)

    def read_page(self, offset):
        """Reads the data from the page at the given offset."""
        page_entry_bytes = self.datafile.read(offset)
        return FlashStore.from_page_bytes(page_entry_bytes)

    @staticmethod
    def to_page_bytes(data):
        """Serializes raw data into a page entry."""
        return FlashStore.get_header(len(data)) + data

    @staticmethod
    def from_page_bytes(page_entry_bytes):
        """Deserializes from a page entry to the raw data."""
        header_size = struct.calcsize("I")
        data_size = struct.unpack(page_entry_bytes[:header_size])
        return page_entry_bytes[header_size : header_size+data_size]

    @staticmethod
    def get_header(data_len):
        """Construct a header given the length of the data."""
        return struct.pack("I", data_len)


class PageFile(object):
    """A simple file that reads and writes at a page granularity."""

    def __init__(self, filepath, pagesize):
        self.datafile = PageFile.open_rw(filepath)
        self.pagesize = pagesize

    def write(self, data, offset):
        """Writes the data to a page at the given offset."""
        if len(data) > self.pagesize:
            raise ValueError("data must fit within page")
        self.datafile.seek(offset*self.pagesize)
        self.datafile.write(data)

    def read(self, offset):
        """Reads the data from the page at the given offset."""
        self.datafile.seek(offset*self.pagesize)
        return self.datafile.read(self.pagesize)

    def close(self):
        """Closes the file, after which no more ops are accepted."""
        self.datafile.close()

    @staticmethod
    def open_rw(filepath):
        """Open a file in rw mode without truncation."""
        try:
            # Open file in rw mode without truncating if it exists.
            return open(filepath, "r+b")
        except IOError:
            # File not found. Truncating is OK.
            return open(filepath, "w+b")
