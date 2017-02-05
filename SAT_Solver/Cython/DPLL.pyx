from functools import reduce
from itertools import takewhile
from random import choice
from copy import deepcopy
from sys import argv


cdef class CNF:
    """
    CNF formula :
        CNF(clause_1, clause_2, ...),
            where clause_i is an iterable of literals,
            each literal being a integer :  > 0 if the polarity of the variable is positive
                                            < 0 otherwise
    """
    cdef list clauses
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

    cdef bint __evaluate_literals(self, bint x, int y):
        global valuation
        return x or (abs(y) in valuation if y >= 0 else not abs(y) in valuation)

    cdef bint __evaluate_clause(self, set c):
        return reduce(self.__evaluate_literals, c, False)

    cdef bint __and_evaluations(self, bint x, set y):
        return x and self.__evaluate_clause(y)

    cdef bint evaluate(self, set valuation):
        return reduce(self.__and_evaluations, self.clauses, True)

    def __len__(self):
        cdef int i
        all_literals = reduce(set.union, self.clauses, set())
        return sum(1 for i in all_literals if i>=0)

    cdef tuple naive_SAT(self):
        cdef int n, N, int_valuation
        cdef bytes binary_valuation
        cdef set valuation
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

    cpdef tuple DPLL(self):
        cdef set suitable_valuation
        cdef list clauses_copy
        suitable_valuation = set()
        clauses_copy = deepcopy(self.clauses)
        return DPLL(clauses_copy, suitable_valuation)


cdef int choose(list clauses):
    return choice(tuple(reduce(set.union, clauses, set())))

cdef bint and_bool_clauses(bint x, set y):
    return x and bool(y)

cdef tuple base_cases(list clauses, set suitable_valuation):
    if not clauses:
        return True, suitable_valuation
    elif not reduce(and_bool_clauses, clauses, True):
        return False, None
    else:
        return ()

cdef set union_unit_clauses(set x, set y):
    return x.union(y) if len(y)==1 else x

cdef tuple DPLL(list clauses, set suitable_valuation):
    cdef tuple base_cases_result, result
    cdef set unit_clauses, negation_unit_clauses, pure_literals, unit_or_pure, neg_unit_or_pure
    cdef int i, index, l, next_literal
    cdef list clauses2

    base_cases_result = base_cases(clauses, suitable_valuation)
    if bool(base_cases_result):
        return base_cases_result

    unit_clauses = reduce(union_unit_clauses, clauses, set())
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

print(CNF(argv[1]).DPLL())
