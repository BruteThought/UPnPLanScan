import urllib
from scrollPad import scrollPad

# Global device directory
devices = {}
selected_device = None


class Device:
    def __init__(self, cache, date, location, opt, nls, server, userAgent, st, usn):
        self.cache = cache
        self.date = date

        # noinspection PyUnresolvedReferences
        parsed_uri = urllib.parse.urlparse(location)
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

    def print_info(self):
        info = "USN: \t\t{0}\n".format(repr(self.usn))
        info += "Cache: \t\t{0}\n".format(repr(self.cache))
        info += "Date: \t\t{0}\n".format(repr(self.date))
        info += "Location: \t{0}\n".format(repr(self.baseURL + self.rootXML))
        info += "Base: \t\t{0}\n".format(repr(self.baseURL))
        info += "Opt: \t\t{0}\n".format(repr(self.opt))
        info += "NLS: \t\t{0}\n".format(repr(self.nls))
        info += "Server: \t{0}\n".format(repr(self.server))
        info += "User Agent: \t{0}\n".format(repr(self.userAgent))
        info += "ST: \t\t{0}\n".format(repr(self.st))
        print(info)
        #scrollPad(stdscr, info)

    def print_services(self, stdscr):
        for service in self.serviceList:
            stdscr.addstr("Service ID:\t {0}\n".format(repr(str(service.id))))
