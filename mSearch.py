from urllib.parse import urlparse
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

    def printinfo(self):
        print("Cache: "+ self.cache)
        print("Date: " + self.date)
        print("Location: " + self.baseURL + self.rootXML)
        print("Opt: " + self.opt)
        print("NLS: " + self.nls)
        print("Server: " + self.server)
        print("User Agent: " + self.userAgent)
        print("ST: " + self.st)
        print("USN: " + self.usn)