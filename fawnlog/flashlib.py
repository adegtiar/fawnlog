"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""


import os
import struct
import threading

from bitarray import bitarray


class ErrorUnwritten(ValueError):
    """The page intended to be read has not yet been written."""


class ErrorFilledHole(ValueError):
    """The page intended to be read or written is a filled hole page."""


class ErrorOverwritten(ValueError):
    """The page intended to be written or filled is already written."""


class PageStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to a fixed address range of pages. Writes must
    fit within a page. Enforces write-once semantics. Internally writes
    the data along with a header.

    """
    # Header consists of the length of the data in that page.
    header = struct.Struct("I")

    def __init__(self, filepath, page_size, num_pages):
        self.page_size = page_size
        self.num_pages = num_pages
        self.unwritten_header = '\x00' * PageStore.header.size
        self.hole_header = PageStore.header.pack(page_size + 1)
        self.lock = threading.Lock()

        self.pagefile = PageFile(filepath, page_size + PageStore.header.size)
        self.written_pages = bitarray(False for page in xrange(num_pages))
        self.hole_pages = set()
        self._init_data(num_pages)

    def write(self, data, offset):
        """Writes the data to a page at the given offset."""
        with self.lock:
            if self.written_pages[offset]:
                raise ErrorOverwritten()
            elif offset in self.hole_pages:
                raise ErrorFilledHole()

            page_entry_bytes = PageStore._pack_data(data)
            self.pagefile.write(page_entry_bytes, offset)

            self.written_pages[offset] = True

    def read(self, offset):
        """Reads the data from the page at the given offset."""
        with self.lock:
            if offset in self.hole_pages:
                raise ErrorFilledHole()
            elif not self.written_pages[offset]:
                raise ErrorUnwritten()

            page_entry_bytes = self.pagefile.read_page(offset)
            return PageStore._unpack_data(page_entry_bytes)

    def fill_hole(self, offset):
        """Fills the page at the given offset with a hole."""
        with self.lock:
            if self.written_pages[offset]:
                raise ErrorOverwritten()

            if offset not in self.hole_pages:
                self.pagefile.write(self.hole_header, offset)
                self.hole_pages.add(offset)

    def close(self):
        """Closes the data store and prevents further operations."""
        with self.lock:
            self.pagefile.close()

    def reset(self):
        """Resets the state of the server, clearing all data."""
        with self.lock:
            self.pagefile.close()
            os.remove(self.pagefile.filepath)
            self.__init__(self.pagefile.filepath, self.page_size, self.num_pages)

    def _init_data(self, num_pages):
        """Processes the given data to build a map of written pages."""
        for pidx, header in self.pagefile.iterpages(PageStore.header.size):
            if header == self.unwritten_header:
                continue
            elif header == self.hole_header:
                self.hole_pages.add(pidx)
            else:
                self.written_pages[pidx] = True

    @staticmethod
    def _pack_data(data):
        """Serializes raw data into a page entry (head + data)."""
        return PageStore.header.pack(len(data)) + data

    @staticmethod
    def _unpack_data(page_bytes):
        """Deserializes from a page entry into the raw data."""
        header_size = PageStore.header.size
        (data_size,) = PageStore.header.unpack(page_bytes[:header_size])
        return page_bytes[header_size:header_size+data_size]


class PageFile(object):
    """A simple file that reads and writes at a page granularity.

    Note: this class is not thread-safe.

    """

    def __init__(self, filepath, pagesize):
        self.datafile = PageFile._open_rw(filepath)
        self.pagesize = pagesize
        self.filepath = filepath

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
        num_bytes = num_bytes or self.pagesize
        self.datafile.seek(offset*self.pagesize)
        return self.datafile.read(num_bytes)

    def close(self):
        """Closes the file, after which no more ops are accepted."""
        self.datafile.close()

    def iterpages(self, num_bytes = None):
        """Iterate over the pages, reading up to num_bytes from each.

        Iterates over (page_id, data) tuples.
        If num_bytes is not specified, reads the entire page each time.

        """
        num_bytes = num_bytes or self.pagesize
        if num_bytes > self.pagesize:
            raise ValueError("num_bytes to read must be <= page size")

        self.datafile.seek(0)
        data = self.datafile.read(num_bytes)
        pidx = 0

        while data:
            yield pidx, data

            # Seek to next page boundary.
            pidx += 1
            self.datafile.seek(self.pagesize - num_bytes, 1)
            data = self.datafile.read(num_bytes)

    @staticmethod
    def _open_rw(filepath):
        """Open a file in rw mode without truncation."""
        try:
            # Open file in rw mode without truncating if it exists.
            return open(filepath, "r+b")
        except IOError:
            # File not found. Truncating is OK.
            return open(filepath, "w+b")
