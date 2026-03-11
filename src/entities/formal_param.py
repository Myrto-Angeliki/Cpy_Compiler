from .entity import Entity

class FormalParameter(Entity):
    def __init__(self, name, dataType=0, mode="cv"):
        super().__init__(name)
        self.dataType = dataType
        self.mode = mode

    def __str__(self):
        return f"{self.name}"