from entities.global_var import GlobalVariable
from entities.function import Function

class FinalGenerator():
    def __init__(self, filename):
        self.f = open(filename, "w")

    def gen_starting_code(self):
        self.produce(f".data \nstr_nl: \n\t.asciz \"\\n\" \n.text\nL0:\n\tj Lmain",False)
        
    def write_function_final(self, funcname, parser, starting_quad, isMain=False):
        linesForFunctionCall = []
        param_count=0 
        indexOfLinesMissingOffset = []
        quadlist = parser.generated_program.programList
 
        for quad in quadlist[starting_quad:]:
            if quad.op !="par" and quad.op !="call": self.produce(f"L{quad.label}:",False)
            if quad.op == "begin_block" and quad.op1 == funcname:
                if isMain:
                    self.produce("Lmain:",False)
                    frameLength = self.find_main_framelength(parser)
                    self.produce(f"addi sp,sp,{frameLength}")
                    self.produce("mv gp,sp")
                else:
                    self.produce(f"sw ra, 0(sp)")
            if quad.op == "end_block" and quad.op1 == funcname:
                if not isMain:
                    self.produce(f"lw ra, 0(sp)")
                    self.produce(f"jr ra\n")
            if self.get_op(quad.op)== "arithmOp":
                self.produce(self.loadvr(quad.op1, "t1", parser))
                self.produce(self.loadvr(quad.op2, "t2", parser))
                self.produce(f"{self.get_arithm_op(quad.op)} t1,t1,t2")
                self.produce(self.storerv("t1", quad.op3, parser))
            if self.get_op(quad.op)=="=":
                self.produce(self.loadvr(quad.op1, "t1", parser))
                self.produce(self.storerv("t1", quad.op3, parser))
            if quad.op == "par":
               if quad.op2 == "cv":
                   param_count += 1
                   if len(linesForFunctionCall) == 0:
                        linesForFunctionCall.append(f"L{quad.label}:\n\taddi fp, sp, ")
                        linesForFunctionCall.append(self.loadvr(quad.op1, "t1", parser))
                   else: linesForFunctionCall.append(("L"+quad.label+":\n\t"+self.loadvr(quad.op1, "t1", parser)))
                   linesForFunctionCall.append("sw t1,-")
                   indexOfLinesMissingOffset.append((len(linesForFunctionCall)-1))
               if quad.op2 == "ret":
                    var, limit = parser.symb_table.search_for_var(quad.op1, parser)
                    if len(linesForFunctionCall) == 0:
                       linesForFunctionCall.append(f"L{quad.label}:\n\taddi fp, sp, ")
                       linesForFunctionCall.append(f"addi t0, sp, -{var.offset}")
                    else: linesForFunctionCall.append(f"L{quad.label}:\n\taddi t0, sp, -{var.offset}")
                    linesForFunctionCall.append("sw t0,-8(fp)")
            if quad.op == "call":
                   func = parser.symb_table.search_for_func(quad.op1, param_count, parser)
                   linesForFunctionCall[0] += str(func.frameLength)
                   for i,j in zip(indexOfLinesMissingOffset,range(0,len(indexOfLinesMissingOffset))):
                       offset = 12 + j*4
                       linesForFunctionCall[i] += f"{str(offset)} (fp)"
                   for line in linesForFunctionCall:
                       if line[0]=="L": self.produce(line,False)
                       else: self.produce(line)
                   linesForFunctionCall = []
                   indexOfLinesMissingOffset = []
                   param_count = 0
                   self.produce(f"L{quad.label}:\n\tsw sp, -4(fp)",False)
                   self.produce(f"addi sp, sp, {func.frameLength}")
                   self.produce(f"jal L{func.startingQuad}")
                   self.produce(f"addi sp, sp, -{func.frameLength}")
            if quad.op == "ret":
                if isMain:
                    self.error("Error: \"return\" can be used only within a function",parser)
                else:   
                    self.produce(self.loadvr(quad.op1, "t1", parser))
                    self.produce("lw t0, -8(sp)\n\tsw t1,0(t0)")
                if quadlist[(int(quad.label)+1)].op !="end_block":
                    self.produce(f"lw ra, 0(sp)")
                    self.produce(f"jr ra")
            if self.get_op(quad.op) == "relOp":
                self.produce(self.loadvr(quad.op1, "t1", parser))
                self.produce(self.loadvr(quad.op2, "t2", parser))
                self.produce(f"{self.getRelop(quad.op)} t1, t2, L{quad.op3}")
            if self.get_op(quad.op) == "j":
                self.produce(f"j L{quad.op3}")
            if quad.op == "in":
                self.produce("li a7, 5\n\tecall")
                self.produce(self.storerv("a0",quad.op1,parser))
            if quad.op == "out":
                self.produce(self.loadvr(quad.op1,"a0",parser))
                self.produce("li a7, 1\n\tecall")
                self.produce("la a0,str_nl\n\tli a7, 4\n\tecall")
            if quad.op == "halt":
                self.produce("li a0,0\n\tli a7,93\n\tecall")

    def produce(self, s, indent=True):
        if indent:
            self.f.write(f"\t{s}\n")
        else:
            self.f.write(f"{s}\n")

    def find_main_framelength(self, parser):
        scopeStack = parser.symb_table.scopeStack[0]
        entityList = scopeStack.entityList
        for i in range((len(entityList)-1),-1,-1): 
            if isinstance(entityList[i], Function):
                continue
            else:
                return (entityList[i].offset + 4)
        return 0

    def gnlvcode(self, var, limit):
        lines_to_write = ""
        lines_to_write += "lw t0,-4(sp)\n"
        i=2
        while i <= limit:
            lines_to_write += "\tlw t0,-4(t0)\n"
            i += 1
        lines_to_write += f"\taddi t0,t0,-{var.offset}\n"
        return lines_to_write

    def loadvr(self, v, r, parser):
        if v.isnumeric():
            return (f"li {r},{v}")
        else:
            var, limit = parser.symb_table.search_for_var(v, parser)
            if isinstance(var, GlobalVariable):
                return (f"lw {r},-{var.offset}(gp)") 
            elif limit == 0:
                return (f"lw {r},-{var.offset}(sp)")
            else:
                return (self.gnlvcode(var, limit)  + (f"\tlw {r},0(t0)") )

    def storerv(self, r, v, parser):
        var, limit = parser.symb_table.search_for_var(v, parser) 
        if isinstance(var, GlobalVariable):
            return (f"sw {r},-{var.offset}(gp)")
        elif limit == 0:
            return (f"sw {r},-{var.offset}(sp)")
        else:
            return (self.gnlvcode(var, limit) + (f"\tsw {r},0(t0)") )
            
    def get_op(self, op):
        if op in ["+","-","//","*","%"]:
            return "arithmOp"
        elif op in ["<",">","<=",">=","!=","=="]:
            return "relOp"
        elif op == "=":
            return op
        elif op == "jump":
            return "j"
        else:
            return None
        
    def get_arithm_op(self,op):
        if op == "+":
            return "add"
        elif op == "-":
            return "sub"
        elif op == "*":
            return "mul"
        elif op == "//":
            return "div"
        else:
            return "rem"

    def getRelop(self, op):
        if op == "<":
            return "blt"
        elif op == ">":
            return "bgt"
        elif op == "<=":
            return "ble"
        elif op == ">=":
            return "bge"
        elif op == "!=":
            return "bne"
        elif op == "==":
            return "beq"
        
    def error(self,s,parser):
        print(f"Error: {s}")
        parser.f_int.write(parser.generated_program.__str__())
        parser.f_symb.write(parser.symb_table.__str__())
        parser.f_symb.close()
        parser.f_int.close()
        exit(0)