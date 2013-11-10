import config


class Projection(object):
    def __init__(self):
        """ flash_number: the number of flash servers
            flash_pages: the number flash pages in a flash server
        """
        self.flash_number = config.FLASH_NUMBER
        self.flash_pages = config.FLASH_PAGES

    def translate(self, pos):
        """ flash servers are divided into groups of two.
            The positions grows round-robinly whithin a group, and grows
              into the next group after filling out the current group.
            Suppose pos is starting from 0.
        """
        if pos >= self.flash_pages * flash_number:
            # todo: garbage collection
            pass

        pos_flash_number = pos // self.flash_pages
        group_number = pos_flash_number // 2
        group_page_number = pos % (self.flash_pages * 2)

        # suppose dest_flash and dest_page are starting from 0
        dest_flash = group_number * 2 + (group_number % 2)
        dest_page = group_page_number // 2

        # if it's the last group, there's a special case that there
        #   is only one server
        if pos_flash_number == self.flash_number - 1:
            if pos_flash_number % 2 == 1:
                dest_flash = self.flash_number - 1
                dest_page = group_page_number

        return (dest_flash, dest_page)
