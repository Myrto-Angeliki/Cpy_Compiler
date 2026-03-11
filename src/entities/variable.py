from .entity import Entity

class Variable(Entity):
    def __init__(self, name, dataType=0, offset=0):
        super().__init__(name)
        self.dataType = dataType
        self.offset = offset

    def __str__(self):
        return f"<----| {self.name}/{self.offset} |"