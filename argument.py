class Argument:
    def __init__(self, name: str, direction: str, relatedStateVariable):
        # TODO: Figure out how to parse retvals! (Part of the UPnP spec)
        # self.retval = retval
        self.name = str(name)
        self.direction = str(direction)
        self.relatedStateVariable = relatedStateVariable
