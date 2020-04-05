import os
import subprocess
import time
import volatile

#run sat solver
def solve(dimacs_cnf):

    input_file = open("input.txt", "w")
    input_file.write(dimacs_cnf)
    input_file.close()

    os.system("minisat input.txt output.txt")

    output_file = open("output.txt", "r")
    result = output_file.read()
    output_file.close()

    return result

#run sat solver given time limit
def timed_solve(dimacs_cnf, timeout):

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
