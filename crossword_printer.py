BLACK_CELL = '/'

#print dimacs results
def output(input, result):

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
                table[i,j] = BLACK_CELL

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

    chars = 0

    for (i,j) in list(result["across"].keys()):
        chars += len(result["across"][i,j])

    for (i,j) in list(result["down"].keys()):
        chars += len(result["down"][i,j])

    print(str(chars)+"/"+str(width*height)+" "+str(chars/(2*width*height)))
