import XMLReader


class action:
    def __init__(self, name, argumentList):
        self.name = name
        self.argumentList = XMLReader.getArguments(argumentList)
