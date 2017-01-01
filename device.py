from urllib.parse import urlparse
from bcolors import bcolors


# noinspection PyPep8Naming
class device:
    def __init__(self, cache, date, location, opt, nls, server, userAgent, st, usn):
        self.cache = cache
        self.date = date

        parsed_uri = urlparse(location)
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

    def printInfo(self):
        print(bcolors.BOLD + "USN: \t\t" + self.usn + bcolors.ENDC)
        print("Cache: \t\t" + self.cache)
        print("Date: \t\t" + self.date)
        print("Location: \t" + self.baseURL + self.rootXML)
        print("Opt: \t\t" + self.opt)
        print("NLS: \t\t" + self.nls)
        print("Server: \t" + self.server)
        print("User Agent: \t" + self.userAgent)
        print("ST: \t\t" + self.st)