class QuadPointerList:
    def __init__(self, label=""):
        self.labelList = []
        if label!="":
            self.labelList.append(label)
        

    def __str__(self) :
        return self.labelList.__str__()
    
    def mergeList(self, list1):
        self.labelList = self.labelList + list1.labelList
    