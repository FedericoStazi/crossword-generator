import input_generator
import cnf_generator
import cnf_parser
import sat_solver
import result_parser
import crossword_printer

import time

#runs the sat solver once
def run_simple(size):

    input = input_generator.generate(size, size)
    cnf = cnf_generator.generate(input)
    dimacs_cnf, var_names = cnf_parser.parse(cnf)
    dimacs_result = sat_solver.solve(dimacs_cnf)

    if dimacs_result is None or dimacs_result.split("\n")[0] == "UNSAT": return

    result = result_parser.parse(input, dimacs_result, var_names)
    crossword_printer.output(input, result)

#runs the sat solver many times, until a solution is found
def run_many_cases(size, timeout):

    print(("*"*20) + "  " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())))

    input = input_generator.generate(size, size)
    cnf = cnf_generator.generate(input)
    dimacs_cnf, var_names = cnf_parser.parse(cnf)
    dimacs_result = sat_solver.timed_solve(dimacs_cnf, timeout)

    if dimacs_result is None:
        return run_many_cases(size, timeout)
    elif dimacs_result.split("\n")[0] == "UNSAT":
        return

    result = result_parser.parse(input, dimacs_result, var_names)
    crossword_printer.output(input, result)

run_many_cases(10, 30*60)
#run_simple(10)
