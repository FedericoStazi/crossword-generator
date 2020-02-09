from random import randint
import string
import os
import subprocess
import time

#generate input informations as a python dict
def input_generator(width, height):

    #TODO get words from a bigger list (check they are lowercase)
    words = ["disk", "moment", "coffee", "thanks", "estate", "tooth", "sample", "insect", "army", "drama", "basket", "coffee", "people", "chest", "lab", "region", "health", "youth", "child", "volume", "bin", "joy", "way", "fit", "new", "van", "eye", "kit", "hut", "era", "tie", "bay", "few", "key", "hot", "job", "dog", "bet", "go", "shy"]
    black_cells = []

    for i in range(3*width):
        black_cells.append((randint(0, width), randint(0, height)))

    input = {}

    input["height"] = width
    input["width"] = height
    input["black_cells"] = black_cells
    input["words"] = words

    return input

#create the c variable as a string
def c(i, j, s, b=0):
    return ("-" if b else "")+"c_"+str(i)+"_"+str(j)+"_"+s

#create the h variable as a string
def h(i, j, w, b=0):
    return ("-" if b else "")+"h_"+str(i)+"_"+str(j)+"_"+str(w)

#create the v variable as a string
def v(i, j, w, b=0):
    return ("-" if b else "")+"v_"+str(i)+"_"+str(j)+"_"+str(w)

#generate cnf using extended format
def cnf_generator(input):

    output = []

    width = input["width"]
    height = input["height"]
    words = input["words"]
    alphabet = (list(string.ascii_lowercase)) + ["/"]

    # black cells
    for (i,j) in input["black_cells"]:
        output.append(c(i,j,'/'))

    # at least one letter in each cell
    for i in range(width):
        for j in range(height):
            letters = []
            for a in alphabet:
                letters.append(c(i,j,a))
            output.append(' '.join(letters))


    # every cell has at most one letter
    for i in range(width):
        for j in range(height):
            for a in alphabet:
                for b in alphabet:
                    if a < b:
                        output.append(c(i,j,a,1) + " " + c(i,j,b,1))

    for w in range(len(words)):

        # word must be in the table
        conditions = []
        for i in range(width):
            for j in range(height):
                conditions.append(h(i,j,w))
                conditions.append(v(i,j,w))
        output.append(' '.join(conditions))

        # word at most once in the table
        for i in range(width):
            for j in range(height):
                for x in range(width):
                    for y in range(height):
                        output.append(h(i,j,w,1) + " " + v(x,y,w,1))
                        if (i,j) > (x,y):
                            output.append(h(i,j,w,1) + " " + h(x,y,w,1))
                            output.append(v(i,j,w,1) + " " + v(x,y,w,1))

        # correct letters
        for i in range(width):
            for j in range(height):

                if i>0:
                    output.append(h(i,j,w,1) + " " + c(i-1,j,'/'))
                for k in range(len(words[w])):
                    output.append(h(i,j,w,1) + " " + c(i+k,j,words[w][k]))
                if i+len(words[w])<width:
                    output.append(h(i,j,w,1) + " " + c(i+len(words[w]),j,'/'))

                if j>0:
                    output.append(v(i,j,w,1) + " " + c(i,j-1,'/'))
                for k in range(len(words[w])):
                    output.append(v(i,j,w,1) + " " + c(i,j+k,words[w][k]))
                if j+len(words[w])<height:
                    output.append(v(i,j,w,1) + " " + c(i,j+len(words[w]),'/'))

        # no words that go out of bounds
        for i in range(width - len(words[w])+1, width):
            for j in range(height):
                output.append(h(i,j,w,1))

        for i in range(width):
            for j in range(height - len(words[w])+1, height):
                output.append(v(i,j,w,1))

    return output

#convert cnf to dimacs format
def cnf_parser(cnf):

    var_list = map((lambda s : s.replace('-', '')),(' '.join(cnf)).split(' '))
    var_names = {}

    curr_var = 0

    for v in var_list:
        if v not in var_names:
            curr_var += 1
            var_names[v] = curr_var

    result = "p cnf "+str(curr_var)+" "+str(len(cnf))+"\n"

    for line in cnf:
        for v in line.split(' '):
            if v[0] == '-':
                result += '-'+str(var_names[v[1:]])+' '
            else:
                result += str(var_names[v])+' '
        result += '0\n'

    return result, var_names

#run sat solver
def sat_solver(dimacs_cnf):

    input_file = open("input.txt", "w")
    input_file.write(dimacs_cnf)
    input_file.close()

    os.system("minisat input.txt output.txt")

    output_file = open("output.txt", "r")
    result = output_file.read()
    output_file.close()

    return result

#run sat solver given time limit
def timed_sat_solver(dimacs_cnf, timeout):

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

#convert dimacs results to python dict
def result_parser(input, dimacs_result, var_names):

    width = input["width"]
    height = input["height"]
    words = input["words"]
    alphabet = (list(string.ascii_lowercase)) + ["/"]

    dimacs_result_list = dimacs_result.split("\n")[1].split(' ')

    result = {}
    result["across"] = {}
    result["down"] = {}

    for i in range(width):
        for j in range(height):
            for w in range(len(words)):
                if h(i,j,w) in var_names and '-'+str(var_names[h(i,j,w)]) not in dimacs_result_list:
                    result["across"][i,j] = words[w]
                if v(i,j,w) in var_names and '-'+str(var_names[v(i,j,w)]) not in dimacs_result_list:
                    result["down"][i,j] = words[w]

    return result

#print dimacs results
def printer(input, result):

    table = {}

    width = input["width"]
    height = input["height"]

    for i in range(width):
        for j in range(height):

            if (i,j) in result["across"]:
                w = result["across"][i,j]
                for k in range(len(w)):
                    table[i+k,j] = w[k]

            if (i,j) in result["down"]:
                w = result["down"][i,j]
                for k in range(len(w)):
                    table[i,j+k] = w[k]


    for i in range(width):
        for j in range(height):
            if (i,j) not in table:
                table[i,j] = '/'

    for i in range(width):
        for j in range(height):
            print(table[(i,j)], end=' ')
        print()

    print("ACROSS")
    for p in result["across"]:
        print(str(p)+": "+str(result["across"][p]))
    print("DOWN")
    for p in result["down"]:
        print(str(p)+": "+str(result["down"][p]))

def run_simple(size):

    input = input_generator(size, size)
    cnf = cnf_generator(input)
    dimacs_cnf, var_names = cnf_parser(cnf)
    dimacs_result = sat_solver(dimacs_cnf)

    if dimacs_result is None or dimacs_result.split("\n")[0] == "UNSAT": return

    result = result_parser(input, dimacs_result, var_names)
    printer(input, result)

run_simple(16)
