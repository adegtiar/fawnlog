"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""

class FlashStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to an infinite address range of pages. Writes must
    fit within a page. Enforces write-once semantics.

    """

    def __init__(self, filepath):
        self.datafile = PageFile(filepath)

    def write_page(self, data, offset):
        """Writes the data to a page at the given offset."""
        pass

    def read_page(self, offset):
        """Reads the data from the page at the given offset."""
        pass


class PageFile(object):
    """A simple file that reads and writes at a page granularity."""

    def __init__(self, filepath, pagesize):
        self.datafile = PageFile.open_rw(filepath)
        self.pagesize = pagesize

    def write_page(self, data, offset):
        """Writes the data to a page at the given offset."""
        pass

    def read_page(self, offset):
        """Reads the data from the page at the given offset."""
        pass


    @staticmethod
    def open_rw(filepath):
        try:
            # Open file in rw mode without truncating if it exists.
            return open(filepath, "r+b")
        except IOError:
            # File not found. Truncating is OK.
            return open(filepath, "w+b")
