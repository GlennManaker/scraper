class matchX:
    def __init__(self, json):
        self.O1 = json['O1']
        self.O2 = json['O2']
        self.I = json['I']
        try:
            self.TS = json['SC']['TS']
            self.S = json['SC']['S']
            if len(self.S) == 0:
                raise RuntimeError("Invalid match")
        except:
            raise RuntimeError("Invalid match")
        try:
            self.S1 = json['SC']['FS']['S1']
        except:
            self.S1 = 0
        try:
            self.S2 = json['SC']['FS']['S2']
        except:
            self.S2 = 0

    def toDict(self):
        return {"I" : self.I, "O1": self.O1, "O2": self.O2, "TS": self.TS,
                     "S": self.S, "S1": self.S1, "S2": self.S2}
