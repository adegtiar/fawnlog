"""The flash-writing back-end library.

Implements the write-once page-based flash interface as a file-backed
data store.

"""

class FlashStore(object):
    """A page-based flash storage interface backed by a file.

    Supports writing to an infinite address range of pages. Writes must
    fit within a page. Enforces write-once semantics.

    """

    def __init__(self, file_path):
        pass

    def write_page(self, data, offset):
        """Writes the data to a page at the given offset."""
        pass

    def read_page(self, offset):
        """Reads the data from the page at the given offset."""
        pass
