class Projection(object):
    """ Projection maps the 64-bit virtual address in the whole log to a
        tuple (dest_host, dest_port, dest_page).

        Currently this mapping is static.

    """
    def __init__(self, config):
        """ Initialize a Projection object.

        flash_page_number: the number of flash pages in a server

        Currently we assum there is no heterogeneity among servers, so we
        remember this configuration.

        """
        self.flash_page_number = config.FLASH_PAGE_NUMBER
        self.flash_per_group = config.FLASH_PER_GROUP
        self.config = config

    def translate(self, token):
        """ Statically translate the 64-bit virtual address in the whole
            log to a tuple (dest_host, dest_port, dest_page). Every token
            corresponds to one page in the cluster.

            The translation works as follows:
            * Flash servers are divided into groups of config.flash_per_group.
            * The positions grows round-robinly whithin a group, and grows
              into the next group after filling out the current group.

            Suppose all variables are starting from 0.

        """
        total_server = len(self.config.SERVER_ADDR_LIST)
        if token >= self.flash_page_number * total_server:
            # todo: garbage collection
            token %= (self.flash_page_number * total_server)

        group_index = token // (self.flash_page_number * self.flash_per_group)
        group_page = token % (self.flash_page_number * self.flash_per_group)

        group_server = 0
        if (group_index + 1) * self.flash_per_group > total_server:
            # if it's the last group, there's a special case that there
            #   is fewer number of servers
            group_server = total_server - group_index * self.flash_per_group
        else:
            group_server = self.flash_per_group

        # get the result
        prev_server = group_index * self.flash_per_group
        dest_server = prev_server + (group_page % group_server)
        dest_page = group_page // group_server

        (dest_host, dest_port) = self.config.SERVER_ADDR_LIST[dest_server]

        return (dest_server, dest_host, dest_port, dest_page)
