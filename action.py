import riskassess


class Action:
    def __init__(self, name: str, argument_list):
        self.name = str(name)
        self.argument_list = argument_list
        self.risk = riskassess.getRisk(self.name)
