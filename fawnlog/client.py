import config
import projection
import sequencer


class Client(object):
    def __init__(self):
        self.sequencer = sequencer.Sequencer()
        self.projection = projection.Projection()

    def append(data):
        """ Assume data is string right now.
            Checking the length of data and get appropriate number
              of position tokens from sequencer
            Every position token got from the sequencer is whithin
              the range of [0, 2^64 - 1]
        """
        # todo: check input
        number_of_tokens = len(data) // config.FLASH_PAGE_SIZE + 1
        pos_list = self.sequencer.get_tokens(number_of_tokens)

        i = 1
        for pos in pos_list:
            beg = (i - 1) * config.FLASH_PAGE_SIZE
            if i < number_of_tokens:
                # not the last one
                end = i * config.FLASH_PAGE_SIZE
                self.write_to(data[beg:end], pos)
            else:
                # the last one
                self.write_to(data[beg:], pos)
            i += 1
        return pos_list

    def write_to(data, pos):
        # data must be fit in a page right now
        # todo: check input
        # todo: write data to server
        (dest_flash, dest_page) = projection.translate(pos)
        return True

    def read(pos):
        # todo: check input
        # todo: read data from server
        (dest_flash, dest_page) = projection.translate(pos)
        return True

    def trim(pos):
        # todo: check input
        return True

    def fill(pos):
        # todo: check input
        data = "".join(["1"] * config.FLASH_PAGE_SIZE)
        self.write_to(data, pos)
