from urllib.parse import urlparse
from bcolors import bcolors


# noinspection PyPep8Naming
class service:
    def __init__(self, deviceType, deviceId, controlURL, eventSubURL, SCPDURL):
        self.type = str(deviceType)
        self.id = str(deviceId)
        self.controlURL = str(controlURL)
        self.eventSubURL = str(eventSubURL)
        parsed_uri = urlparse(SCPDURL)
        self.SCPDURL = str('{uri.path}'.format(uri=parsed_uri).strip("/"))
        self.actionList = []
        self.riskRanking = 0

    def printInfo(self, stdscr):
        stdscr.addstr("\tserviceType:\t" + self.type)
        stdscr.addstr("\tserviceId:\t" + self.id)
        stdscr.addstr("\tcontrolURL:\t" + self.controlURL)
        stdscr.addstr("\teventSubURL:\t" + self.eventSubURL)
        stdscr.addstr("\tSCPDURL:\t" + "/" + self.SCPDURL)
        stdscr.refresh()

    def printActions(self):
        for action in self.actionList:
            print(bcolors.OKGREEN + "\t\t└ Action: {0}".format(action.name) + bcolors.ENDC)
            for argument in action.argumentList:
                if type(argument.relatedStateVariable) is not str:
                    print(bcolors.WARNING + "\t\t  {:4} {:32} {:10} {}".format(argument.direction,
                                                                           argument.name,
                                                                           argument.relatedStateVariable.dataType,
                                                                           argument.relatedStateVariable.defaultValue) + bcolors.ENDC)
                else:
                    print(bcolors.WARNING + "\t  {0}\t {1}".format(argument.direction,
                                                                       argument.name) + bcolors.ENDC)
