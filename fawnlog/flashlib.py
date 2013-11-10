"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""


import struct


class PageStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to an infinite address range of pages. Writes must
    fit within a page. Enforces write-once semantics.

    """
    header = struct.Struct("I")

    def __init__(self, filepath, page_size):
        self.datafile = PageFile(filepath, page_size + PageStore.header.size)

    def write(self, data, offset):
        """Writes the data to a page at the given offset."""
        page_entry_bytes = PageStore.to_page_bytes(data)
        self.datafile.write(page_entry_bytes, offset)

    def read(self, offset):
        """Reads the data from the page at the given offset."""
        page_entry_bytes = self.datafile.read_page(offset)
        return PageStore.from_page_bytes(page_entry_bytes)

    def close(self):
        """Closes the data store and prevents further operations."""
        self.datafile.close()

    @staticmethod
    def to_page_bytes(data):
        """Serializes raw data into a page entry."""
        return PageStore.header.pack(len(data)) + data

    @staticmethod
    def from_page_bytes(page_bytes):
        """Deserializes from a page entry to the raw data."""
        header_size = PageStore.header.size
        (data_size,) = PageStore.header.unpack(page_bytes[:header_size])
        return page_bytes[header_size:header_size+data_size]


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

    def read_page(self, offset):
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
