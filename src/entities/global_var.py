from .variable import Variable

class GlobalVariable(Variable):
    def __init__(self, name, dataType=0, offset=0):
        super().__init__(name, dataType, offset)

    def __str__(self):
        return f"<-----| {self.name}/{self.offset} |"