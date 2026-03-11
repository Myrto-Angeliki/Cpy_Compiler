from .variable import Variable

class TemporaryVariable(Variable):
    def __init__(self, name, dataType=0, offset=0):
        super().__init__(name, dataType, offset)