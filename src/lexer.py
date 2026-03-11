from token import Token

LETTER = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
DIGIT = ["0","1","2","3","4","5","6","7","8","9"]
WC = [" ","\t","\n","\r"]
GROUP_SYMBOL = ["{","}","(",")"]
DELIMETER = [",",":"]
MUL_OP = ["*","%","/"]
ADD_OP = ["+","-"]
ASSIGNMENT = ["="]
REL_OP = ["<",">","!"]
COMMENT = ["#"]
EOF = ["eof"]
ERRORS = {-1:"invalid symbol",-2:"number out of bounds [-32767,32767]",-3:"an identifier can't be longer than 30 characters",
          -4:"invalid symbol after '#'",-5:"comments never closed",-6:"no letters are allowed inside a number",
          -7:"symbol '/' must be followed by '/'",-8:"only '#int' and '#def' are allowed",-9:"symbol '!' must be followed by '='"}
KEYWORDS = ["def","while","print","if","elif","else","return","int","input","and","or","not","#int","#def","main","global"]
ALPHABET = LETTER + DIGIT + WC + GROUP_SYMBOL + DELIMETER + MUL_OP + ADD_OP + ASSIGNMENT + REL_OP + COMMENT + EOF
SYMBOLS = {"a":0,"b":0,"c":0,"d":0,"e":0,"f":0,"g":0,"h":0,"i":0,"j":0,"k":0,"l":0,"m":0,
               "n":0,"o":0,"p":0,"q":0,"r":0,"s":0,"t":0,"u":0,"v":0,"w":0,"x":0,"y":0,"z":0,
               "A":0,"B":0,"C":0,"D":0,"E":0,"F":0,"G":0,"H":0,"I":0,"J":0,"K":0,"L":0,"M":0,
               "N":0,"O":0,"P":0,"Q":0,"R":0,"S":0,"T":0,"U":0,"V":0,"W":0,"X":0,"Y":0,"Z":0,
               "0":1,"1":1,"2":1,"3":1,"4":1,"5":1,"6":1,"7":1,"8":1,"9":1,"*":2,"%":2,"/":3,
               "+":4,"-":4,"=":5,"<":6,">":7,"!":8,",":9,":":9,"#":10,"(":11,")":11,"eof":12,
               " ":13,"\t":13,"\n":13,"\r":13,'{':14,'}':14,"other":15}

class Lexer:
    
    
    def __init__(self, file_name): 
        self.current_line = 1
        self.file_name = file_name
        self.bytes_read = 0
        self.next_state = [[1, 2, 300, 3, 400, 4, 5, 6, 7,700, 8,800, 1000, 0, -1, -1],
                           [1,1,100,100,100,100,100,100,100,100,100,100,100,100,100,100],
                           [-6, 2,200,200,200,200,200,200,200,200,200,200,200,200,200,200],
                           [-7, -7, -7, 300, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7, -7],
                           [500,500,500,500,500,600,500,500,500,500,500,500,500,500,500,500],
                           [600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600],
                           [600,600,600,600,600,600,600,600,600,600,600,600,600,600,600,600],
                           [-9,-9,-9,-9,-9,600,-9,-9,-9,-9,-9,-9,-9,-9,-9,-9],
                           [11,-4,-4,-4,-4,-4,-4,-4,-4,-4, 9,-4,-4,-4,800,-4],
                           [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 9,-5, 9, 9, 9],
                           [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, -5, 9, 9, 9],
                           [11,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,-8,900,900,-8,-8]]
        self.token = Token("", "", 1)

    def next_token(self):
        global WC
        global SYMBOLS
        global KEYWORDS
        global ALPHABET
        global ERRORS

        current_state = 0
        f = open(self.file_name, "rb")
        f.seek(self.bytes_read)
        self.token = Token("","",self.current_line)

        while True:
            c = (f.read(1)).decode("utf-8")
            self.bytes_read += 1
            
            if c == '':
                c = "eof"
            if c not in ALPHABET:
               self.token.recognized_string = c
               c = "other"

            self.token.line_number = self.current_line

            previous_state = current_state
            current_state = self.next_state[current_state][SYMBOLS[c]]

            if (previous_state==8 and current_state==9) or (previous_state==9 and current_state==9) or (previous_state==9 and current_state==10) \
                or (previous_state==10 and current_state==9) or (previous_state==10 and current_state==0):
                self.token.recognized_string = ""
                if c == "\n":
                    self.current_line += 1
                continue

            if current_state == 100:
                self.bytes_read -= 1
                if len(self.token.recognized_string)>30:
                    current_state = -3
                elif self.token.recognized_string in KEYWORDS:
                    self.token.family = "keyword"
                    return self.token
                else:
                    self.token.family = "id" 
                    return self.token
            if current_state == 200:
                self.bytes_read -= 1
                self.token.family = "number"
                num = int(self.token.recognized_string)
                if num<-32767 or num>32767:
                    current_state = -2
                else:
                    return self.token
            if current_state == 300:
                self.token.recognized_string = self.token.recognized_string + c
                self.token.family = "mulOp"
                return self.token
            if current_state == 400:
                self.token.family = "addOp"
                self.token.recognized_string = c
                return self.token
            if current_state == 500:
                self.bytes_read -= 1
                self.token.family = "assignment" 
                return self.token
            if current_state == 600:
                temp = self.token.recognized_string + c
                if temp not in ["!=","<=",">=","=="]:
                    self.bytes_read -= 1
                else:
                    self.token.recognized_string = self.token.recognized_string + c    
                self.token.family = "relOp"
                return self.token
            if current_state == 700:
                self.token.recognized_string = c
                self.token.family = "delimeter"
                return self.token
            if current_state == 800:
                self.token.family = "groupSymbol"
                self.token.recognized_string = self.token.recognized_string + c
                return self.token
            if current_state == 900:
                if self.token.recognized_string not in ["#int","#def"]:
                    current_state = -8
                else:
                    self.token.family = "keyword"
                    return self.token
            if current_state == 1000:
                self.token.family = "eof"
                return self.token
            if current_state < 0:
                self.token.family = "error"
                s =  ERRORS[current_state]
                self.error(s, self.current_line)
                return self.token
            if c not in WC:
                self.token.recognized_string += c
            if c == "\n":
                self.current_line += 1

    def error(self, string, line):
        print(("Error: "+string + ", line "+str(line)))
        exit(0)
