import var_to_string as vts
import string

#return true if i,j is inside the table, false otherwise
def inside(i,j,w,h):
    return i>=0 and i<w and j>=0 and j<h

#generate cnf using extended format
def generate(input):

    alphabet = (list(string.ascii_lowercase)) + [vts.BLACK_CELL]

    output = []

    width = input["width"]
    height = input["height"]

    words = input["words"]
    words_flat = [item for sublist in input["words"] for item in sublist]

    additional = input["additional"]

    # iff conditions for H
    for i in range(width):
        for j in range(height):
            conditions = [vts.H(i,j,1)]
            for w in range(len(words_flat)):
                conditions.append(vts.h(i,j,w))
            output.append(' '.join(conditions))

    for i in range(width):
        for j in range(height):
            for w in range(len(words_flat)):
                output.append(vts.h(i,j,w,1) + ' ' + vts.H(i,j))

    # iff conditions for V
    for i in range(width):
        for j in range(height):
            conditions = [vts.V(i,j,1)]
            for w in range(len(words_flat)):
                conditions.append(vts.v(i,j,w))
            output.append(' '.join(conditions))

    for i in range(width):
        for j in range(height):
            for w in range(len(words_flat)):
                output.append(vts.v(i,j,w,1) + ' ' + vts.V(i,j))

    # 2 or more consecutive letters are part of a word
    for i in range(width):
        for j in range(height):

            if inside(i+1,j,width,height):
                output.append(
                    ((vts.c(i-1,j,vts.BLACK_CELL,1)+' ') if inside(i-1,j,width,height) else '')+
                    vts.c(i,j,vts.BLACK_CELL) + ' ' +
                    vts.c(i+1,j,vts.BLACK_CELL) + ' ' +
                    vts.H(i,j)
                )

            if inside(i,j+1,width,height):
                output.append(
                    ((vts.c(i,j-1,vts.BLACK_CELL,1)+' ') if inside(i,j-1,width,height) else '')+
                    vts.c(i,j,vts.BLACK_CELL) + ' ' +
                    vts.c(i,j+1,vts.BLACK_CELL) + ' ' +
                    vts.V(i,j)
                )

    # at least one symbol in each cell
    for i in range(width):
        for j in range(height):
            letters = []
            for a in alphabet:
                letters.append(vts.c(i,j,a))
            output.append(' '.join(letters))


    # every cell has at most one symbol
    for i in range(width):
        for j in range(height):
            for a in alphabet:
                for b in alphabet:
                    if a < b:
                        output.append(vts.c(i,j,a,1) + ' ' + vts.c(i,j,b,1))

    # one word for each group must be in the table
    conditions = []
    offset = 0
    for g in range(len(words)):
        group = words[g]
        for w in range(len(group)):
            for i in range(width):
                for j in range(height):
                    conditions.append(vts.h(i,j,offset+w))
                    conditions.append(vts.v(i,j,offset+w))
        offset += len(group)
        output.append(' '.join(conditions))
        conditions = []

    for w in range(len(words_flat)):

        # word at most once in the table
        for i in range(width):
            for j in range(height):
                for x in range(width):
                    for y in range(height):
                        output.append(vts.h(i,j,w,1) + " " + vts.v(x,y,w,1))
                        if (i,j) > (x,y):
                            output.append(vts.h(i,j,w,1) + " " + vts.h(x,y,w,1))
                            output.append(vts.v(i,j,w,1) + " " + vts.v(x,y,w,1))

        # correct letters
        for i in range(width):
            for j in range(height):

                if i>0:
                    output.append(vts.h(i,j,w,1) + " " + vts.c(i-1,j,vts.BLACK_CELL))
                for k in range(len(words_flat[w])):
                    output.append(vts.h(i,j,w,1) + " " + vts.c(i+k,j,words_flat[w][k]))
                if i+len(words_flat[w])<width:
                    output.append(vts.h(i,j,w,1) + " " + vts.c(i+len(words_flat[w]),j,vts.BLACK_CELL))

                if j>0:
                    output.append(vts.v(i,j,w,1) + " " + vts.c(i,j-1,vts.BLACK_CELL))
                for k in range(len(words_flat[w])):
                    output.append(vts.v(i,j,w,1) + " " + vts.c(i,j+k,words_flat[w][k]))
                if j+len(words_flat[w])<height:
                    output.append(vts.v(i,j,w,1) + " " + vts.c(i,j+len(words_flat[w]),vts.BLACK_CELL))

        # no words that go out of bounds
        for i in range(width - len(words_flat[w])+1, width):
            for j in range(height):
                output.append(vts.h(i,j,w,1))

        for i in range(width):
            for j in range(height - len(words_flat[w])+1, height):
                output.append(vts.v(i,j,w,1))

    for condition in additional:
        output.append(condition)

    return output
