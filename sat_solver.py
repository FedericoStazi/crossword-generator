import os
import subprocess
import time

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

    input_file = open("input.txt", "w")
    input_file.write(dimacs_cnf)
    input_file.close()

    #adding exec makes kill work (https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true)
    proc = subprocess.Popen("exec " + "minisat -verb=0 input.txt output.txt > /dev/null", shell=True)

    try:

        proc.communicate(timeout=timeout)

        output_file = open("output.txt", "r")
        result = output_file.read()

        output_file.close()
        return result

    except subprocess.TimeoutExpired:

        proc.kill()
        proc.communicate()
        return None
