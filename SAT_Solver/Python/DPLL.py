from functools import reduce
from itertools import takewhile
from random import choice
from copy import deepcopy
import sys


class CNF():
    """
    CNF formula :
        CNF(clause_1, clause_2, ...),
            where clause_i is an iterable of literals,
            each literal being a integer :  > 0 if the polarity of the variable is positive
                                            < 0 otherwise
    """
    def __init__(self, *args):
        assert args
        self.clauses = [set()]
        if isinstance(args[0], str):
            with open(args[0]) as f:
                for line in f:
                    if line[0] == 'c' or line[0] == 'p':
                        continue
                    line = map(int, line.split())

                    for var in line:
                        # Add variable numbers until 0 is reached
                        if isinstance(var, int) and var!=0:
                            self.clauses[-1].add(var)
                        # Up until the end of the line : add the remainder to a new clause (corresponding to a new set in self.clauses)
                        elif var == 0:
                            self.clauses.append(set())
                        else:
                            break

            if not self.clauses[-1]:
                del self.clauses[-1]

        else:
            self.clauses = list(set(c) for c in args)

    def __str__(self):
        s=''
        if not self.clauses:
            s='     '
        for clause in self.clauses:
            s += ' || '.join(map(str, clause)) + '\t & \t'
        return s[:-5]

    def __nonzero__(self):
        return self.clauses != 0

    def __iter__(self):
        for c in self.clauses:
            yield c

    def evaluate(self, valuation):
        def evaluate_clause(c):
            return reduce(lambda x, y: x or (abs(y) in valuation if y >= 0 else not abs(y) in valuation), c, False)

        return reduce(lambda x, y: x and evaluate_clause(y), self.clauses, True)

    def __len__(self):
        all_literals = reduce(set.union, self.clauses, set())
        return sum(1 for i in all_literals if i>=0)

    def naive_SAT(self):
        n = len(self)
        N = 2**n

        for int_valuation in range(N):
            binary_valuation = ("{:0"+str(n)+"b}").format(int_valuation)
            valuation = {index+1 for index, val in enumerate(binary_valuation) if bool(int(val))}
            if self.evaluate(valuation):
                break
        else:
            return False, None
        return True, valuation

    def DPLL(self):
        suitable_valuation = set()
        clauses_copy = deepcopy(self.clauses)
        return DPLL(clauses_copy, suitable_valuation)

def choose(clauses, choice = 'default'):
    if choice == 'random':
        return choice(tuple(reduce(set.union, clauses, set())))
    else:
        return next(iter(clauses[0]))

def DPLL(clauses, suitable_valuation=set()):
    def base_cases(clauses, suitable_valuation):
        if not clauses:
            return True, suitable_valuation
        elif not reduce(lambda x, y: x and bool(y), clauses, True):
            return False, None
        else:
            return ()

    base_cases_result = base_cases(clauses, suitable_valuation)
    if base_cases_result:
        return base_cases_result

    unit_clauses = reduce(lambda x, y: x.union(y) if len(y)==1 else x, clauses, set())
    negation_unit_clauses = set(-i for i in unit_clauses)
    pure_literals = reduce(set.intersection, clauses)

    unit_or_pure = pure_literals | unit_clauses
    neg_unit_or_pure = pure_literals | negation_unit_clauses

    if unit_clauses & negation_unit_clauses:
        return False, None

    if unit_or_pure:
        for index, clause in enumerate(clauses):
            if unit_clauses & clause:
                clauses[index] = None
            else:
                clause -= neg_unit_or_pure
        clauses = [s for s in clauses if s is not None]

    suitable_valuation.update((l for l in unit_or_pure if l >= 0))

    base_cases_result = base_cases(clauses, suitable_valuation)
    if base_cases_result:
        return base_cases_result

    next_literal = choose(clauses)

    clauses2 = deepcopy(clauses)
    for index, clause in enumerate(clauses):
        if next_literal in clause:
            clauses[index] = None
            clauses2[clauses2.index(clause)].remove(next_literal)
        elif -next_literal in clause:
            clauses2[clauses2.index(clause)] = None
            clause.remove(-next_literal)
    clauses = [s for s in clauses if s is not None]
    clauses2 = [s for s in clauses2 if s is not None]

    result = DPLL(clauses, suitable_valuation.union((abs(next_literal),) if next_literal >= 0 else ()))
    if result[0]:
        return result
    else:
        return DPLL(clauses2, suitable_valuation.union((abs(next_literal),) if next_literal < 0 else ()))

# tests = []
# tests.append(CNF((1,-2,-3),(-1,2,-3), (3,)))
# tests.append(CNF((1,),(-1,)))
# tests.append(CNF((1,-1), (2,)))
# tests.append(CNF("./test2.txt"))
# tests.append(CNF("./test6.txt"))
#
#
# for t in tests:
#     print(t)
#     print(t.DPLL())

print(CNF(sys.argv[1]).DPLL())
