import os
import subprocess
import time
import volatile

from pysat.formula import CNF
from pysat.solvers import Minisat22

from multiprocessing import Pool

#run sat solver
def solve_bash(dimacs_cnf):

    with volatile.file(mode = 'w') as input_file, volatile.file(mode = 'r') as output_file:

        input_file.write(dimacs_cnf)
        input_file.close()

        os.system("minisat " + input_file.name + " " + output_file.name)

        result = output_file.read()
        output_file.close()

        return result

#run sat solver given time limit
def timed_solve_bash(dimacs_cnf, timeout):

    with volatile.file(mode = 'w') as input_file, volatile.file(mode = 'r') as output_file:

        input_file.write(dimacs_cnf)
        input_file.close()

        #adding exec makes kill work (https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true)
        proc = subprocess.Popen("exec " + "minisat -verb=0 " + input_file.name + " " + output_file.name + " > /dev/null", shell=True)

        try:

            proc.communicate(timeout=timeout)

            result = output_file.read()
            output_file.close()

            return result

        except subprocess.TimeoutExpired:

            output_file.close()

            proc.kill()
            proc.communicate()

            return None

#solve using pysat
def solve(dimacs_cnf):

    with Minisat22() as m:

        cnf = CNF(from_string = dimacs_cnf)

        m.append_formula(cnf)
        m.solve()

        print(m.get_model()[:100])

        return "SAT\n" + (" ".join(str(n) for n in m.get_model())) + " 0";

#solve using pysat given time limit
def timed_solve(dimacs_cnf, timeout):

    with Pool() as pool:

        result = pool.apply_async(solve, (dimacs_cnf,))
        result.wait(timeout)

        return result.get() if result.ready() else None
