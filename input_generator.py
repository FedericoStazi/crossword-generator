import var_to_string as vts

import json
import random

#generate input informations as a python dict

def generate(width, height):

    optional = []

    for i in range(width):
        optional.append(vts.H(i, 0, 1))
        optional.append(vts.H(i, height - 1, 1))

    for j in range(height):
        optional.append(vts.V(0, j, 1))
        optional.append(vts.V(width - 1, j, 1))

    count = {
        '2': (1, 1),
        '3': (6, 1),
        '4': (4, 1),
        '5': (3, 2),
        '6': (2, 2),
        '7': (1, 2)
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
    input["optional"] = optional

    return input
