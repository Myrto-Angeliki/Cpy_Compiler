from sym_table.scope import Scope
from entities import *

class Table():
    def __init__(self):
        self.scopeStack = []
        self.nextLevel = 0

    def __str__(self):
        str = ""
        for i in range((len(self.scopeStack)-1),-1,-1):
            str += (self.scopeStack[i].__str__()+"\n")
        return str
 
    def add_scope(self):
        scope = Scope(self.nextLevel)
        self.nextLevel += 1
        self.scopeStack.append(scope)

    def remove_scope(self):
        scope = self.scopeStack.pop()
        self.nextLevel -= 1
        return scope
    
    def add_entity(self, entity):
        if self.scopeStack != []:
            self.scopeStack[-1].entityList.append(entity)
            
    def create_var(self, name):
        var = Variable(name,offset=self.scopeStack[-1].current_offset)
        return var
    
    def add_vars(self, vars):
        if vars != []:
            for var in vars:
                self.add_entity(self.create_var(var))
                self.scopeStack[-1].current_offset += 4
    
    def create_global_var(self, name):
        var = GlobalVariable(name,offset=self.scopeStack[-1].current_offset)
        return var
    
    def add_global_vars(self, global_vars):
        if global_vars != []:
            for var in global_vars:
                self.add_entity(self.create_global_var(var))
                self.scopeStack[-1].current_offset += 4

    def add_temp_var(self, temp_name):
        self.add_entity(TemporaryVariable(temp_name,offset=self.scopeStack[-1].current_offset))
        self.scopeStack[-1].current_offset += 4
    
    def add_formal_params(self, formal_params):
        if formal_params != []:
            for param in formal_params:
                parameter = Parameter(param, offset=self.scopeStack[-1].current_offset)
                formal_param = FormalParameter(parameter)
                self.add_entity(parameter)
                self.scopeStack[-2].entityList[-1].formalParameters.append(formal_param)
                self.scopeStack[-1].current_offset += 4

    def update_framelength(self):
        self.scopeStack[-2].entityList[-1].frameLength = self.scopeStack[-1].current_offset 

    def update_starting_quad(self, label):
        self.scopeStack[-2].entityList[-1].startingQuad = label

    def add_func(self, name):
        func = Function(name)
        self.add_entity(func)
    
    def add_global_vars_to_func(self, global_vars):
        self.scopeStack[-2].entityList[-1].globalVars = global_vars

    def get_func_globals(self):
        global_vars = []
        if len(self.scopeStack)>1:
            if self.scopeStack[-2].entityList != []:
                global_vars = self.scopeStack[-2].entityList[-1].globalVars
        return global_vars

    def search_for_var(self, var, parser):
        for i in range((len(self.scopeStack)-1),-1,-1):
            scope = self.scopeStack[i]
            limit = (len(self.scopeStack)-1) - i
            for existing_entity in scope.entityList:
                if var == existing_entity.name:
                    if isinstance(existing_entity,Variable) or isinstance(existing_entity,Parameter) or isinstance(existing_entity,TemporaryVariable):
                        return existing_entity, limit
                    if isinstance(existing_entity,GlobalVariable) :
                            global_vars = self.get_func_globals()
                            if var in global_vars or len(self.scopeStack)==1:
                                return existing_entity, limit
                            else:
                                self.error(f"Missing global declaration for {var}",parser)
        self.error((f"Variable {var} is undefined"),parser)

    def search_for_func(self, func_name, param_count, parser):
        for i in range((len(self.scopeStack)-1),-1,-1):
            scope = self.scopeStack[i]
            for existing_entity in scope.entityList:
                if func_name == existing_entity.name:
                    if isinstance(existing_entity,Function):
                        expected_count =len(existing_entity.formalParameters) 
                        if expected_count==param_count:
                            return existing_entity
                        else:
                            self.error(f"Missing arguments while calling {func_name}(): {func_name}() expected {expected_count} arguments but found {param_count} instead",parser)
        self.error((f"Function {func_name} is undefined"),parser)
                    
    def error(self, strn, parser):
        print("Error: "+strn)
        parser.f_int.write(parser.generated_program.__str__())
        parser.f_symb.write(parser.symb_table.__str__())
        parser.f_symb.close()
        parser.f_int.close()
        exit(0)