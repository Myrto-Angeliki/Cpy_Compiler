from .formal_param import FormalParameter

class Parameter(FormalParameter):
    def __init__(self, name, mode="cv", dataType=0, offset=0):
        super().__init__(name, dataType, mode)
        self.offset = offset

    def __str__(self):
        return f"<----| {self.name}/{self.offset}/{self.mode} |"