# Class for parsing arguments for services provided by devices
class Argument:
    def __init__(self, name: str, direction: str, related_state_variable):
        # TODO: Figure out how to parse retvals! (Part of the UPnP spec)
        # self.retval = retval
        self.name = str(name)
        self.direction = str(direction)
        self.related_state_variable = related_state_variable
