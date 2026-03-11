class Quad():
    def __init__(self, label, op, op1, op2, op3):
        self.label = label
        self.op = op
        self.op1 = op1 
        self.op2 = op2
        self.op3 = op3

    def __str__(self):
        return  (self.label+": "+self.op+", "+ self.op1+", "+self.op2+", "+self.op3)
        
    def returnLabel(self):
        return self.label