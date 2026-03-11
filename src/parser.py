import sys
from pathlib import Path

from token import Token
from lexer import Lexer
from intermediate.quad_list import QuadList
from intermediate.quad_ptr_list import QuadPointerList
from sym_table.table import Table
from final_gen import FinalGenerator

token = Token("","",0)

class Parser:
    
    def __init__(self, filename, target_file="..//assembly_files//final.asm"):
        self.lexical_analyzer = Lexer(filename)
        self.generated_program = QuadList()
        self.symb_table = Table()
        self.temp_counter = 0
        self.f_symb = open(".\\sym_table\\symbols_table.sym","w")
        self.f_int = open(".\\intermediate\\intermediate.int", "w")
        self.final_gen = FinalGenerator(target_file)

    def new_temp(self):
        temp_name = f"T_{self.temp_counter}"
        self.symb_table.add_temp_var(temp_name)
        self.temp_counter += 1
        return temp_name
    
    def empty_list(self):
        return QuadPointerList()
    
    def make_list(self, label):
        return QuadPointerList(label)


    def analyze_syntax(self):
        global token
        token = self.get_token()
        self.start_rule()
        print("Compilation successfully completed.")

    def get_token(self):
        return self.lexical_analyzer.next_token()
    
    def error(self,string):
        print("Error: "+string + ", line "+str(self.lexical_analyzer.current_line))
        self.symb_table.remove_scope()
        self.f_int.write(self.generated_program.__str__())
        self.f_symb.write(self.symb_table.__str__())
        self.f_symb.close()
        self.f_int.close()
        exit(0)
    
    def start_rule(self):
        self.generated_program.genQuad("jump","_","_","main")
        self.final_gen.gen_starting_code()
        self.symb_table.add_scope()

        global_vars = self.declarations()
        self.symb_table.add_global_vars(global_vars)

        self.defs()

        self.f_symb.write(self.symb_table.__str__())
        self.symb_table.remove_scope()
        self.f_int.write(self.generated_program.__str__())
        self.f_symb.close()
        self.f_int.close()
        self.final_gen.f.close()

    def defs(self):
        global token

        if token.recognized_string=="def":
            self.funcdef()
            self.defs()
        elif token.recognized_string=="#def":
            self.maindef()
        elif token.family=="eof":
                self.error(" Missing main definition")
        else:
            self.error(" "+token.recognized_string+" violates the program structure\n"+"Program structure: top->global variables, middle->function definitions, bottom->main definition")

    def funcdef(self):
        global token

        token = self.get_token()
        if token.family=="id":
            func_name = token.recognized_string
            self.symb_table.add_func(func_name)
            token = self.get_token()
            if token.recognized_string=='(':
                token = self.get_token()
                formal_params = self.idList()
                self.symb_table.add_scope()
                self.symb_table.add_formal_params(formal_params)
                if token.recognized_string==')':
                    token = self.get_token()
                    if token.recognized_string==':':
                        token = self.get_token()
                        if token.recognized_string=='#{':
                            token = self.get_token()
                            vars = self.declarations()
                            self.symb_table.add_vars(vars)   
                            while token.recognized_string=="def":
                                self.funcdef()
                            global_vars = self.global_variables()
                            self.symb_table.add_global_vars_to_func(global_vars)
                            starting_quad = self.generated_program.quadCounter
                            self.symb_table.update_starting_quad(starting_quad) 
                            self.generated_program.genQuad("begin_block",func_name,"_","_")
                            self.statements()
                            if token.recognized_string=='#}': 
                                self.generated_program.genQuad("end_block",func_name,"_","_")
                                token = self.get_token()
                                self.symb_table.update_framelength()
                                self.f_symb.write(self.symb_table.__str__())
                                self.f_symb.write("------------------------------\n")
                                self.final_gen.write_function_final(func_name, self, starting_quad)
                                self.symb_table.remove_scope()
                            else:
                                self.error(" missing '#}'")
                        else:
                            self.error(" missing '#{'")
                    else:
                        self.error(" missing ':'")
                else:
                    self.error(" missing ')'")
            else:
                self.error(" missing '('")
        else:
            self.error(" function name is not valid")

    def maindef(self):
        global token

        token = self.get_token()
        if token.recognized_string=="main":
            starting_quad = self.generated_program.quadCounter
            self.generated_program.genQuad("begin_block","main","_","_") 

            token = self.get_token()
            
            vars = self.declarations()
            self.symb_table.add_vars(vars)

            self.statements()
            
            if token.family=="eof":
                self.generated_program.genQuad("halt","_","_","_") 
                self.generated_program.genQuad("end_block","main","_","_")
                self.final_gen.write_function_final("main", self, starting_quad,True)
                return
            else:
                self.error(" No function definitions allowed after main")
        else:
            self.error(" Correct main definition is '#def main'")

    def global_variables(self):
        global token
        global_vars = []
        
        while token.recognized_string=="global":
            token = self.get_token()
            names = self.idList()
            if names == []:
                self.error("Expected global variable name after \"global\" keyword")
            global_vars = global_vars + names
        return global_vars


    def declarations(self):
        global token
        names = []
        
        while token.recognized_string=="#int":
            token = self.get_token()
            names = names + self.idList()
        return names

    def idList(self):
        global token
        names = []

        if token.family=='id':
            names.append(token.recognized_string)
            token = self.get_token()
            while token.recognized_string==',':
                token = self.get_token()
                if token.family != 'id':
                    self.error(" Expected ID after ','")
                names.append(token.recognized_string)
                token = self.get_token()
        return names
        
    def statements(self):
        global token
        stat_keywords = ["print","return","if","while"]

        if token.family!="eof" and token.recognized_string!="#}":
            self.statement()
            while token.family=="id" or token.recognized_string in stat_keywords:
                self.statement()
        else:
            self.error(" At least one statement is required")


    def statement(self):
        global token

        if self.simple_statement()!=-1:
            return
        elif self.complex_statement()!=-1:
            return
        else:
            self.error(" Unrecognized statement "+token.recognized_string)

    def simple_statement(self):
        global token

        res = 0
        if token.family=="id":
            target = token.recognized_string
            token = self.get_token()
            A_place = self.assignment_stat()
            self.generated_program.genQuad("=",A_place,"_",target)
        elif token.recognized_string=="print":
            token = self.get_token()
            self.print_stat()
        elif token.recognized_string=="return":
            token = self.get_token()
            self.return_stat()
        else:
            res = -1
        return res

    def complex_statement(self):
        global token

        res = 0
        if token.recognized_string=="if":
            token = self.get_token()
            self.if_stat()
        elif token.recognized_string=="while":
            token = self.get_token()
            self.while_stat()
        else:
            res = -1
        return res

    def assignment_stat(self):
        global token
        if token.recognized_string=="=":
            token = self.get_token()
            E_place = self.expression()
            return E_place
        else:
            self.error((" Expected '=' but got '"+token.recognized_string+"'"))


    def print_stat(self):
        global token

        if token.recognized_string=="(":
            token = self.get_token()
            E_place = self.expression()
            self.generated_program.genQuad("out",E_place,"_","_")
            if token.recognized_string==")":
                token = self.get_token()
            else:
                self.error((" Missing ')'"))
        else:
            self.error((" Missing '('"))


    def return_stat(self):
        E_place = self.expression()
        self.generated_program.genQuad("ret",E_place,"_","_")

    def if_stat(self):
        global token
        
        condition_false, condition_true = self.condition()
        if token.recognized_string==":":
            self.generated_program.backPatch(condition_true, self.generated_program.nextQuad())
            token = self.get_token()
            if token.recognized_string=="#{":
                token = self.get_token()
                self.statements()
                if token.recognized_string=="#}":
                    ifList = self.make_list(self.generated_program.nextQuad())
                    self.generated_program.genQuad("jump","_","_","_")
                    self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
                    token = self.get_token()
                else:
                    self.error((" Missing '#}'"))
            else:
                self.statement()
                ifList = self.make_list(self.generated_program.nextQuad())
                self.generated_program.genQuad("jump","_","_","_")
                self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
        else:
           self.error((" Missing ':'")) 

        elif_exitList = self.elifpart()
        self.elsepart()
 
        self.generated_program.backPatch(ifList, self.generated_program.nextQuad())
        if elif_exitList != None:
            self.generated_program.backPatch(elif_exitList, self.generated_program.nextQuad())
        


    def elifpart(self):
        global token
        exitList = self.empty_list()

        while token.recognized_string=="elif":
            token = self.get_token()
            condition_false, condition_true = self.condition()
            if token.recognized_string==":":
                self.generated_program.backPatch(condition_true, self.generated_program.nextQuad())
                token = self.get_token()
                if token.recognized_string=="#{":
                    token = self.get_token()
                    self.statements()
                    if token.recognized_string=="#}":
                        t = self.make_list(self.generated_program.nextQuad())
                        self.generated_program.genQuad("jump","_","_","_")
                        exitList.mergeList(t)
                        self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
                        token = self.get_token()
                    else:
                        self.error((" Missing '#}'"))
                else:
                    self.statement()
                    t = self.make_list(self.generated_program.nextQuad())
                    self.generated_program.genQuad("jump","_","_","_")
                    exitList.mergeList(t)
                    self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
            else:
                self.error(("Missing ':'")) 

        return exitList

    def elsepart(self):
        global token

        if token.recognized_string=="else":
            token = self.get_token()
            if token.recognized_string==":":
                token = self.get_token()
                if token.recognized_string=="#{":
                    token = self.get_token()
                    self.statements()
                    if token.recognized_string=="#}":
                        token = self.get_token()
                    else:
                        self.error((" Missing '#}'"))
                else:
                    self.statement()
            else:
                self.error((" Missing ':'")) 


    def while_stat(self):
        global token

        condQuad = self.generated_program.nextQuad()
        condition_false, condition_true = self.condition()
        if token.recognized_string==":":
            self.generated_program.backPatch(condition_true, self.generated_program.nextQuad())
            token = self.get_token()
            if token.recognized_string=="#{":
                token = self.get_token()
                self.statements()
                if token.recognized_string=="#}":
                    self.generated_program.genQuad("jump","_","_",condQuad)
                    self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
                    token = self.get_token()
                else:
                    self.error((" Missing '#}'"))
            else:
                self.statement()
                self.generated_program.genQuad("jump","_","_",condQuad) 
                self.generated_program.backPatch(condition_false, self.generated_program.nextQuad())
        else:
            self.error((" Missing ':'")) 

    def expression(self):
        global token

        optional_sign = self.optional_sign()
        T1_place = self.term()
        if(optional_sign!=""):
            w = self.new_temp()
            self.generated_program.genQuad(optional_sign,"0", T1_place, w)
            T1_place = w

        while token.family=="addOp":
            addOp = token.recognized_string
            token = self.get_token()
            T2_place = self.term()
            w = self.new_temp()
            self.generated_program.genQuad(addOp,T1_place, T2_place, w)
            T1_place = w

        E_place = T1_place
        return E_place

    def optional_sign(self):
        global token
        OP_place = ""

        if token.family=="addOp":
            OP_place = token.recognized_string
            token = self.get_token()
        return OP_place

    def term(self):
        global token

        F1_place = self.factor()

        while token.family=="mulOp":
            mulOp = token.recognized_string
            token = self.get_token()
            F2_place = self.factor()
            w = self.new_temp()
            self.generated_program.genQuad(mulOp,F1_place, F2_place, w)
            F1_place = w

        T_place = F1_place
        return T_place


    def factor(self):
        global token
        F_place = ""
        if token.family=="number":
            F_place = token.recognized_string
            token = self.get_token()
            return F_place
        elif token.family=="id":
            F_place = token.recognized_string
            token = self.get_token()
            retVar = self.idtail()
            if retVar != "":
                self.generated_program.genQuad("call",F_place,"_","_")
                return retVar
            return F_place
        elif token.recognized_string=="(":
            token = self.get_token()
            F_place = self.expression()
            if token.recognized_string==")":
                token = self.get_token()
                return F_place
            else:
                self.error((" Missing ')'"))
        elif token.recognized_string=="int":
            token = self.get_token()
            self.user_input()
            F_place = self.new_temp()
            self.generated_program.genQuad("in",F_place,"_","_")
            return F_place
        else:
            self.error((" expected an expression but got: "+token.recognized_string))
        return F_place

    def user_input(self):
        global token

        if token.recognized_string=="(":
            token = self.get_token()
            if token.recognized_string=="input":
                token = self.get_token()
                if token.recognized_string=="(":
                    token = self.get_token()
                    if token.recognized_string==")":
                        token = self.get_token()
                        if token.recognized_string==")":
                            token = self.get_token()
                            return
                        else:
                            self.error((" Missing ')'"))
                    else:
                        self.error((" Missing ')'"))
                else:
                    self.error((" Missing '('"))
            else:
                self.error((" Expected 'input' but got '"+token.recognized_string+"'"))
        else:
            self.error((" Missing '('"))

    def idtail(self):
        global token
        retVar = ""

        if token.recognized_string=="(":
            token = self.get_token()
            self.actual_par_list()
            if token.recognized_string==")":
                retVar = self.new_temp()
                self.generated_program.genQuad("par",retVar,"ret","_")
                token = self.get_token()
                return retVar
            else:
                self.error((" Missing ')'"))
                
        return retVar
        
    def actual_par_list(self):
        global token

        if token.recognized_string==")":
            return 
        E_place = self.expression()
        self.generated_program.genQuad("par",E_place,"cv","_")
        while token.recognized_string==",":
            token = self.get_token()
            E_place = self.expression()
            self.generated_program.genQuad("par",E_place,"cv","_")

    def condition(self):
        global token

        C_false, C_true = self.boolterm()
        while token.recognized_string=="or":
            self.generated_program.backPatch(C_false, self.generated_program.nextQuad())
            token = self.get_token()
            BT2_false, BT2_true = self.boolterm()
            C_true.mergeList(BT2_true)
            C_false = BT2_false

        return C_false, C_true

    def boolterm(self):
        global token

        BT_false, BT_true = self.boolfactor()
        while token.recognized_string=="and":
            self.generated_program.backPatch(BT_true, self.generated_program.nextQuad())
            token = self.get_token()
            BF2_false, BF2_true = self.boolfactor()
            BT_false.mergeList(BF2_false)
            BT_true = BF2_true

        return BT_false, BT_true
        
    def boolfactor(self):
        global token

        if token.recognized_string=="not":
            token = self.get_token()  
            E1_place = self.expression()
            if token.family=="relOp":
                relop = token.recognized_string
                token = self.get_token()
                E2_place = self.expression()
                boolFactor_false = self.make_list(self.generated_program.nextQuad())
                self.generated_program.genQuad(relop,E1_place,E2_place,"_")
                boolFactor_true = self.make_list(self.generated_program.nextQuad())
                self.generated_program.genQuad("jump","_","_","_")

                return boolFactor_false, boolFactor_true
            else:
                self.error((" Expected relative operator but got: "+token.recognized_string))
        else:
            E1_place = self.expression()
            if token.family=="relOp":
                relop = token.recognized_string
                token = self.get_token()
                E2_place = self.expression()
                boolFactor_true = self.make_list(self.generated_program.nextQuad())
                self.generated_program.genQuad(relop,E1_place,E2_place,"_")
                boolFactor_false = self.make_list(self.generated_program.nextQuad())
                self.generated_program.genQuad("jump","_","_","_")

                return boolFactor_false, boolFactor_true
            else:
                self.error((" Expected relative operator but got: "+token.recognized_string))    



def main(argv):
    if len(argv) < 2:
        Parser("..\\cpy_programs\\default_test.cpy").analyze_syntax()
    else:
        try:
            relative = Path(argv[1])
            absolute = relative.absolute() 
            Parser(absolute).analyze_syntax()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main(sys.argv)