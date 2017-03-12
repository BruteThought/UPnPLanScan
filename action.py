import riskassess

class Action:
    def __init__(self, name, argumentList):
        self.name = name
        self.argumentList = argumentList
        self.risk = riskassess.getRisk(self.name)
