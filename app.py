import input_generator
import cnf_generator
import cnf_parser
import sat_solver
import result_parser
import crossword_printer

import time
import sys

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
def run_many_cases(height, width, timeout):

    print(("*"*20) + "  " + str(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())))

    input = input_generator.generate(height, width)
    cnf = cnf_generator.generate(input)
    dimacs_cnf, var_names = cnf_parser.parse(cnf)
    dimacs_result = sat_solver.timed_solve(dimacs_cnf, timeout)

    if dimacs_result is None:
        return run_many_cases(height, width, timeout)
    elif dimacs_result.split("\n")[0] == "UNSAT":
        return

    # debug print, bug not solved yet...
    if len(dimacs_result.split("\n")) < 2:
        print(dimacs_result.split("\n"))

    result = result_parser.parse(input, dimacs_result, var_names)
    crossword_printer.output(input, result)

# test version of linear_search
def linear_search(height, width, next, timeout):

    while height > 0 and width > 0:

        print("height = "+str(height)+" width = "+str(width))

        run_many_cases(width, height, timeout)

        height, width = next(height, width)


minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 10
linear_search(8, 16, lambda x,y : (x-1,y-2), minutes * 60)
