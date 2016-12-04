# noinspection PyPep8Naming
class service:
    def __init__(self, deviceType, deviceId, controlURL, eventSubURL, SCPDURL):
        self.type = deviceType
        self.id = deviceId
        self.controlURL = controlURL
        self.eventSubURL = eventSubURL
        self.SCPDURL = SCPDURL
        self.actionList = []
        self.riskRanking = 0

    def printInfo(self):
        print("serviceType:\t" + self.type)
        print("serviceId:\t" + self.id)
        print("controlURL:\t" + self.controlURL)
        print("eventSubURL:\t" + self.eventSubURL)
        print("SCPDURL:\t" + self.SCPDURL + "\n")
