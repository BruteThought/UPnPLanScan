class mSearch:
    def __init__(self, cache, date, location, opt, nls, server, userAgent, st, usn):
        self.cache = cache
        self.date = date
        self.location = location
        self.opt = opt
        self.nls = nls
        self.server = server
        self.userAgent = userAgent
        self.st = st
        self.usn = usn

    def printinfo(self):
        print("----START DEVICE INFO----")
        print("Cache: "+ self.cache)
        print("Date: " + self.date)
        print("Location: " + self.location)
        print("Opt: " + self.opt)
        print("NLS: " + self.nls)
        print("Server: " + self.server)
        print("User Agent: " + self.userAgent)
        print("ST: " + self.st)
        print("USN: " + self.usn)
        print("----END DEVICE INFO----")

    def getLocation(self):
        return self.location