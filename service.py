class service:
    def __init__(self, type, id, controlURL, eventSubURL, SCPDURL):
        self.type = type
        self.id = id
        self.controlURL = controlURL
        self.eventSubURL = eventSubURL
        self.SCPDURL = SCPDURL

    def printInfo(self):
        print("serviceType:\t" + self.type)
        print("serviceId:\t\t" + self.id)
        print("controlURL:\t\t" + self.controlURL)
        print("eventSubURL:\t" + self.eventSubURL)
        print("SCPDURL:\t\t" + self.SCPDURL)