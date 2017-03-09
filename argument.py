class Argument:
    def __init__(self, name, direction, relatedStateVariable):
        # TODO: Figure out how to parse retvals! (Part of the UPnP spec)
        # self.retval = retval
        self.name = name
        self.direction = direction
        self.relatedStateVariable = relatedStateVariable
