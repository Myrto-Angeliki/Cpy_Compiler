class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return f'{self.recognized_string}\t\tfamily:\"{self.family}\",\tline: {self.line_number}'

