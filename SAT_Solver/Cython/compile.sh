python setup.py build_ext --inplace 2>&1> /dev/null && python -c "from DPLL import CNF; print(CNF('$1').DPLL())"
