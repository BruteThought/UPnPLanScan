import urllib


class Device:
    def __init__(self, cache, date, location, opt, nls, server, userAgent, st, usn):
        self.cache = cache
        self.date = date

        # noinspection PyUnresolvedReferences
        parsed_uri = urllib.urlparse(location)
        self.baseURL = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # Remove the leading slash, this is already covered in the base URL
        self.rootXML = '{uri.path}'.format(uri=parsed_uri).strip("/")

        self.opt = opt
        self.nls = nls
        self.server = server
        self.userAgent = userAgent
        self.st = st
        self.usn = usn
        self.serviceList = []

    def printInfo(self, stdscr):
        stdscr.addstr("USN: \t\t{0}\n".format(repr(self.usn)))
        stdscr.addstr("Cache: \t\t{0}\n".format(repr(self.cache)))
        stdscr.addstr("Date: \t\t{0}\n".format(repr(self.date)))
        stdscr.addstr("Location: \t{0}\n".format(repr(self.baseURL + self.rootXML)))
        stdscr.addstr("Base: \t{0}\n".format(repr(self.baseURL)))
        stdscr.addstr("Opt: \t\t{0}\n".format(repr(self.opt)))
        stdscr.addstr("NLS: \t\t{0}\n".format(repr(self.nls)))
        stdscr.addstr("Server: \t{0}\n".format(repr(self.server)))
        stdscr.addstr("User Agent: \t{0}\n".format(repr(self.userAgent)))
        stdscr.addstr("ST: \t\t{0}\n".format(repr(self.st)))
        stdscr.refresh()

    def printServices(self, stdscr):
        for service in self.serviceList:
            stdscr.addstr("Service ID:\t {0}\n".format(repr(str(service.id))))