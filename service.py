from urllib.parse import urlparse
from bcolors import bcolors


# noinspection PyPep8Naming
class service:
    def __init__(self, deviceType, deviceId, controlURL, eventSubURL, SCPDURL):
        self.type = deviceType
        self.id = deviceId
        self.controlURL = controlURL
        self.eventSubURL = eventSubURL
        parsed_uri = urlparse(SCPDURL)
        self.SCPDURL = '{uri.path}'.format(uri=parsed_uri).strip("/")
        self.actionList = []
        self.riskRanking = 0

    def printInfo(self):
        print("\tserviceType:\t" + self.type)
        print("\tserviceId:\t" + self.id)
        print("\tcontrolURL:\t" + self.controlURL)
        print("\teventSubURL:\t" + self.eventSubURL)
        print("\tSCPDURL:\t" + self.SCPDURL)

    def printActions(self):
        for action in self.actionList:
            print(bcolors.OKGREEN + "\t\t└ Action: {0}".format(action.name) + bcolors.ENDC)
