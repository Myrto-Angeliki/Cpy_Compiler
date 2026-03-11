from .entity import Entity

class Function(Entity):
    def __init__(self, name, dataType=0, startingQuad="_", frameLength="_"):
        super().__init__(name)
        self.dataType = dataType
        self.startingQuad = startingQuad
        self.frameLength = frameLength
        self.formalParameters = []
        self.globalVars = []


    def __str__(self) -> str:
        str = f"<------| {self.name}/{self.startingQuad}/{self.frameLength} |<{len(self.formalParameters)}>"
        return str

