import json
import random

#generate input informations as a python dict

def generate(width, height):

    black_cells = []

    black_cells.append((0, 0))
    black_cells.append((0, height - 1))
    black_cells.append((width - 1, 0))
    black_cells.append((width - 1, height - 1))

    words_file = open("words.txt")
    all_words = json.loads(words_file.read())
    words_file.close()

    count = {
        '2': (4, 1),
        '3': (5, 1),
        '4': (4, 1),
        '5': (3, 2),
        '6': (2, 2),
        '7': (1, 2)
    }

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
    input["black_cells"] = black_cells
    input["words"] = words

    return input
