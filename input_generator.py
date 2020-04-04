import json
import random

#generate input informations as a python dict

def generate(width, height):

    #TODO get words from a bigger list (check they are lowercase)
    black_cells = []

    for i in range(0):
        black_cells.append((randint(0, width), randint(0, height)))

    words_file = open("words.txt")
    all_words = json.loads(words_file.read())
    words_file.close()

    count = {
        '2': (5, 1),
        '3': (5, 1),
        '4': (6, 1),
        '5': (3, 1),
        '6': (1, 2),
        '7': (1, 2)
    }

    words = []
    for x in count.keys():
        total, group_size = count[x]
        for t in range(total):
            group = []
            for i in range(group_size):
                group.append(random.choice(all_words[x]))
            words.append(group)

    input = {}

    input["height"] = width
    input["width"] = height
    input["black_cells"] = black_cells
    input["words"] = words

    return input
