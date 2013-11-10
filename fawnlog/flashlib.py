"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""


import struct


class ErrorUnwritten(ValueError):
    """The page intended to be read has not yet been written."""


class ErrorOverwritten(ValueError):
    """The page intended to be written has already been written."""


class PageStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to an infinite address range of pages. Writes must
    fit within a page. Enforces write-once semantics. Internally writes
    the data along with a header.

    """
    # Header consists of the length of the data in that page.
    header = struct.Struct("I")

    def __init__(self, filepath, page_size):
        self.datafile = PageFile(filepath, page_size + PageStore.header.size)
        self.init_data() # Initialize self.datamap.

    def write(self, data, offset):
        """Writes the data to a page at the given offset."""
        if offset in self.datamap:
            raise ErrorOverWritten()

        page_entry_bytes = PageStore.to_page_bytes(data)
        self.datafile.write(page_entry_bytes, offset)

        self.datamap.add(offset)

    def read(self, offset):
        """Reads the data from the page at the given offset."""
        if offset not in self.datamap:
            raise ErrorUnwritten()

        page_entry_bytes = self.datafile.read_page(offset)
        return PageStore.from_page_bytes(page_entry_bytes)

    def close(self):
        """Closes the data store and prevents further operations."""
        self.datafile.close()

    def init_data(self):
        """Processes the given data to build a map of written pages."""
        datamap = set() # TODO: make this more efficient (bitarray?).
        header_size = PageStore.header.size

        for pidx, page_data in enumerate(self.datafile.iterpages(header_size)):
            datamap.add(pidx)

        self.datamap = datamap

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

    def read_page(self, offset, num_bytes = None):
        """Reads a page of data at the given offset.

        If num_bytes is specified, reads that many bytes instead of a
        full page.

        """
        if num_bytes is None:
            num_bytes = self.pagesize

        self.datafile.seek(offset*self.pagesize)
        return self.datafile.read(num_bytes)

    def close(self):
        """Closes the file, after which no more ops are accepted."""
        self.datafile.close()

    def iterpages(self, num_bytes = None):
        """Iterates over the page data, reading up to num_bytes bytes.

        If num_bytes is not specified, reads the entire page each time.

        """
        if num_bytes is None:
            num_bytes = self.pagesize
        elif num_bytes > self.pagesize:
            raise ValueError("num_bytes to read must be <= page size")

        empty_page = '\x00' * num_bytes
        self.datafile.seek(0)
        data = self.datafile.read(num_bytes)

        while data:
            if data != empty_page:
                yield data

            # Seek to next page boundary.
            self.datafile.seek(self.pagesize - num_bytes, 1)
            data = self.datafile.read(num_bytes)

    @staticmethod
    def open_rw(filepath):
        """Open a file in rw mode without truncation."""
        try:
            # Open file in rw mode without truncating if it exists.
            return open(filepath, "r+b")
        except IOError:
            # File not found. Truncating is OK.
            return open(filepath, "w+b")
