import var_to_string as vts

import json
import random

def _additional(width, height):

    additional = []

    for i in range(width):
        additional.append(vts.H(i, 0, 1))
        additional.append(vts.H(i, height - 1, 1))

    for j in range(height):
        additional.append(vts.V(0, j, 1))
        additional.append(vts.V(width - 1, j, 1))

    return additional

#generate input informations as a python dict

def generate(width, height):

    count = {
        '2': (1, 1), #1
        '3': (4, 1), #6
        '4': (4, 1), #4
        '5': (3, 2), #3
        '6': (2, 2), #2
        '7': (1, 2)  #1
    }

    words_file = open("words.txt")
    all_words = json.loads(words_file.read())
    words_file.close()

    words = []
    for x in count.keys():
        total, group_size = count[x]
        words_size_x = random.sample(all_words[x], total * group_size)
        for t in range(total):
            words.append(words_size_x[group_size*t:group_size*(t+1)])

    print(words)

    input = {}

    input["height"] = width
    input["width"] = height
    input["words"] = words
    input["additional"] = _additional(height, width)

    return input
