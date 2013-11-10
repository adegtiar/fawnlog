import config


class Projection(object):
    """ Projection maps the 64-bit virtual address in the whole log to a
        tuple (dest_host, dest_port, dest_page).

        Currently this mapping is static.

    """
    def __init__(self):
        """ Initialize a Projection object.

        flash_page_number: the number of flash pages in a server

        Currently we assum there is no heterogeneity among servers, so we
        remember this configuration.

        """
        self.flash_page_number = config.FLASH_PAGE_NUMBER

    def translate(self, token):
        """ Statically translate the 64-bit virtual address in the whole
            log to a tuple (dest_host, dest_port, dest_page). Every token
            corresponds to one page in the cluster.

            The translation works as follows:
            * Flash servers are divided into groups of two.
            * The positions grows round-robinly whithin a group, and grows
              into the next group after filling out the current group.

            Suppose all variables are starting from 0.

        """
        number_of_servers = len(config.SERVER_HOST_LIST)
        if token >= self.flash_page_number * number_of_servers:
            # todo: garbage collection
            token %= (self.flash_page_number * number_of_servers)

        group_number = token // (self.flash_page_number * 2)
        group_page = token % (self.flash_page_number * 2)

        # get the result
        if (group_number + 1) * 2 > number_of_servers:
            # if it's the last group, there's a special case that there
            # is only one server in this group
            dest_server = number_of_servers - 1
            dest_page = group_page
        else:
            dest_server = group_number * 2 + (group_page % 2)
            dest_page = group_page // 2

        dest_host = config.SERVER_HOST_LIST[dest_server]
        dest_port = config.SERVER_PORT_LIST[dest_server]

        return (dest_host, dest_port, dest_page)
