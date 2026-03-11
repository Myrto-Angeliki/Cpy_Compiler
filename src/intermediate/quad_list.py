from intermediate.quad import Quad

class QuadList:
    def __init__(self) :
        self.programList = []
        self.quadCounter = 0
    
    def __str__(self):
        list_contents = ""
        for quad in self.programList:
            list_contents += quad.__str__() + "\n"
        return list_contents
    
    def backPatch(self, quadPointerList, label) :
        if quadPointerList == None:
            return
        for l in quadPointerList.labelList:
            for quad in self.programList:
                if l==quad.label:
                    quad.op3 = label
    
    def genQuad(self, op, op1, op2, op3):
        self.programList.append(Quad(str(self.quadCounter), op, op1, op2, op3))
        self.quadCounter += 1

    def nextQuad(self):
        return str(self.quadCounter)