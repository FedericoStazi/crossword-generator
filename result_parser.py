import var_to_string as vts
import string

BLACK_CELL = '/'

#convert dimacs results to python dict
def parse(input, dimacs_result, var_names):

    width = input["width"]
    height = input["height"]
    words_flat = [item for sublist in input["words"] for item in sublist]
    alphabet = (list(string.ascii_lowercase)) + [BLACK_CELL]

    dimacs_result_list = dimacs_result.split("\n")[1].split(' ')

    result = {}
    result["across"] = {}
    result["down"] = {}

    for i in range(width):
        for j in range(height):
            for w in range(len(words_flat)):
                if vts.h(i,j,w) in var_names and '-'+str(var_names[vts.h(i,j,w)]) not in dimacs_result_list:
                    result["across"][i,j] = words_flat[w]
                if vts.v(i,j,w) in var_names and '-'+str(var_names[vts.v(i,j,w)]) not in dimacs_result_list:
                    result["down"][i,j] = words_flat[w]

    return result
