from entities import Entity

class Scope():
    def __init__(self, level, current_offset=12):
        self.level = level
        self.entityList = []
        self.current_offset = current_offset

    def __str__(self):
        str = f"( {self.level} )"
        for entity in self.entityList:
            str += entity.__str__()
        return str