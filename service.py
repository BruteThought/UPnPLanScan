from urllib.parse import urlparse
import curses


class Service:
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
        stdscr.addstr("serviceType:\t{0}\n".format(repr(str(self.type))))
        stdscr.addstr("serviceId:\t{0}\n".format(repr(str(self.id))))
        stdscr.addstr("controlURL:\t{0}\n".format(repr(str(self.controlURL))))
        stdscr.addstr("eventSubURL:\t{0}\n".format(repr(str(self.eventSubURL))))
        stdscr.addstr("SCPDURL:\t{0}\n".format(repr(str("/" + self.SCPDURL))))
        stdscr.refresh()

    def printActions(self, stdscr):
        for action in self.actionList:
            stdscr.addstr("Action: {0}\n".format(action.name), curses.A_BOLD)
            for argument in action.argumentList:
                if type(argument.relatedStateVariable) is not str:
                    stdscr.addstr("\t{:4} {:32} {:10} {}\n".format(argument.direction,
                                                                   argument.name,
                                                                   argument.relatedStateVariable.dataType,
                                                                   argument.relatedStateVariable.defaultValue))
                else:
                    stdscr.addstr("{0}\t {1}\n".format(argument.direction, argument.name))
