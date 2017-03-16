import urllib
import curses
import riskassess
from scrollPad import scrollPad


class Service:
    def __init__(self, deviceType, deviceId, controlURL, eventSubURL, SCPDURL):
        self.type = str(deviceType)
        self.id = str(deviceId)
        self.controlURL = str(controlURL)
        self.eventSubURL = str(eventSubURL)
        # noinspection PyUnresolvedReferences
        parsed_uri = urllib.parse.urlparse(SCPDURL)
        self.SCPDURL = str('{uri.path}'.format(uri=parsed_uri).strip("/"))
        self.actionList = []
        self.risk = riskassess.getRisk(self.type)

    def printInfo(self, stdscr):
        scrollPad(stdscr, self.getInfoString())

    def getInfoString(self) -> str:
        output = "serviceType:\t{0}\n".format(repr(str(self.type)))
        output += "serviceId:\t{0}\n".format(repr(str(self.id)))
        output += "controlURL:\t{0}\n".format(repr(str(self.controlURL)))
        output += "eventSubURL:\t{0}\n".format(repr(str(self.eventSubURL)))
        output += "SCPDURL:\t{0}\n".format(repr(str("/" + self.SCPDURL)))
        return output

    def printActions(self, stdscr):
        output = self.getInfoString()
        output += "\n"
        for action in self.actionList:
            output += "Actions: {0}\n".format(action.name)
            for argument in action.argumentList:
                if type(argument.relatedStateVariable) is not str:
                    output += "\t{:4} {:32} {:10} {}\n".format(argument.direction,
                                                                   argument.name,
                                                                   argument.relatedStateVariable.dataType,
                                                                   argument.relatedStateVariable.defaultValue)
                else:
                    output += "{0}\t {1}\n".format(argument.direction, argument.name)
        scrollPad(stdscr, output)
