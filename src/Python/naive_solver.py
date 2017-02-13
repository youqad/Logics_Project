from functools import reduce

class Boolexpr():
    """
    Boolean expression : 
        Boolexpr(operator, arguments), 
            where operator in {"or", "and", "not", "var"}
    """
    def __init__(self, operator, *args):
        self.operator = operator.lower()
        self.arguments = set(args)
        
    def __str__(self, indent=1):
        
        s = self.operator
        
        if self.arguments:
            s += '\n'
            
        for arg in self.arguments:
            s += '\t'*indent
            if isinstance(arg, Boolexpr):
                s+=arg.__str__(indent=indent+1)
            else:
                s+=str(arg)
            s+= '\n'
        return s
    
    def __iter__(self):
        if self.operator == 'var':
            yield next(iter(self.arguments))
        else:
            yield self.operator
            for arg in self.arguments:
                yield next(arg)
    
    def evaluate(self, valuation):
        
        if self.operator == 'var':
            return valuation[next(iter(self.arguments))-1]
        elif self.operator == 'not':
            return not (next(iter(self.arguments)).evaluate(valuation))
        elif self.operator == 'or':
            return reduce(lambda x, y: x or y, (arg.evaluate(valuation) for arg in self.arguments))
        elif self.operator == 'and':
            return reduce(lambda x, y: x and y, (arg.evaluate(valuation) for arg in self.arguments))
    
    def __len__(self):
        return sum(1 for operator in self if isinstance(operator, int))
                
    def naive_SAT(self):
        n = len(self)
        N = 2**n
        
        for int_valuation in range(N):
            binary_valuation = ("{:0"+str(n)+"b}").format(int_valuation)
            valuation = [bool(int(i)) for i in binary_valuation]
            if self.evaluate(valuation):
                break
        else:
            return False, None
        return True, binary_valuation
        
        
test = Boolexpr("And", Boolexpr("Or", Boolexpr("Not",Boolexpr("Var", 1)), Boolexpr("Not",Boolexpr("Var", 2))), Boolexpr("Var", 3))
test2 = Boolexpr("And", Boolexpr("Var", 1), Boolexpr("Not",Boolexpr("Var", 1)))

print(test)

print(test.evaluate([True, False, True]))

print(test.evaluate([False, True, False]))

print(test.naive_SAT())
print(test2.naive_SAT())