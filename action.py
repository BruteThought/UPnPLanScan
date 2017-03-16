import riskassess


class Action:
    def __init__(self, name: str, argumentList):
        self.name = str(name)
        self.argumentList = argumentList
        self.risk = riskassess.getRisk(self.name)
