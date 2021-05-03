# cellular automata but with hypercubes
# how many are active at 6th boot cycle?

# input
with open('17.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one row of cubes
input_list = list(input.split('\n'))

# turn each row into a list, so hypercube_start has a list of lists
# (hypercube_start is a plane)
hypercube_start = [list(row) for row in input_list]

# one more dimension to get the space
space = [hypercube_start]

# another dimension to get the hyperspace
hypercubes = [space]
# [[[['#', '.', '.', '.', '.', '#', '.', '#'],
#    ['.', '.', '#', '#', '.', '#', '#', '.'],
#    ['#', '.', '.', '#', '.', '.', '#', '.'],
#    ['.', '#', '.', '.', '#', '.', '.', '#'],
#    ['.', '#', '.', '.', '#', '.', '.', '.'],
#    ['#', '#', '.', '#', '#', '#', '#', '#'],
#    ['#', '.', '.', '#', '.', '.', '#', '.'],
#    ['#', '#', '.', '#', '#', '.', '.', '#']]]]

# states given:
# active = #
# inactive = .

# to avoid deep copies, i'm going to introduce two more states:
# I = currently inactive, will become active
# A = currently active, will become inactive

# CA rules:
# active + number of active next to it is NOT 2 or 3 => inactive
# inactive + three active next to it => active


# adds the surrounding environment to the space
# hypercubes = [...,space,...]
# space = [...,plane,...]
# plane = [...,row,...]
# row = [...,hypercube,...]
def add_environment(hypercubes):
    W = len(hypercubes) # number of spaces in a hyperspace
    Z = len(hypercubes[0]) # number of planes in a space
    Y = len(hypercubes[0][0]) # number of rows in a plane
    X = len(hypercubes[0][0][0]) # number of hypercubes in a row
    # a hypercube is hypercubes[][][][]
    # surround each row: one . either side (L and R)
    for w in range(0,W):
        for z in range(0,Z):
            for y in range(0,Y):
                # hypercubes[w][z][y] is a row
                hypercubes[w][z][y] = ['.'] + hypercubes[w][z][y] + ['.']
    X += 2 # added two more hypercubes to each row
    # surround each plane: one row of . either side (T and Bo)
    for w in range(0,W):
        for z in range(0,Z):
            # hypercubes[w][z] is a plane
            hypercubes[w][z] = [['.']*X] + hypercubes[w][z] + [['.']*X]
    Y += 2 # added two more rows to each plane
    # surround each space with two planes of . (F and Ba)
    for w in range(0,W):
        # hypercubes[w] is a space
        hypercubes[w] = [[['.']*X for y in range(0,Y)]] + hypercubes[w] + [[['.']*X for y in range(0,Y)]]
    Z += 2 # added two more planes to each space
    # surround the hyperspace with two spaces of . (Be and A)
    hypercubes = [[[['.']*X for y in range(0,Y)] for z in range(0,Z)]] + hypercubes + [[[['.']*X for y in range(0,Y)] for z in range(0,Z)]]
    W += 2 # added two more spaces to the hyperspace
    return hypercubes

# gets states of adjacent hypercubes
def get_adj(x,y,z,w):
    offsets = [-1,0,1]
    adj_states = []
    W = len(hypercubes) # number of spaces in a hyperspace
    Z = len(hypercubes[0]) # number of planes in a space
    Y = len(hypercubes[0][0]) # number of rows in a plane
    X = len(hypercubes[0][0][0]) # number of hypercubes in a row
    for i in offsets:
        for j in offsets:
            for k in offsets:
                for l in offsets:
                    # if in range (note: will be done after adding environment)
                    if x+i in range(0,X) and y+j in range(0,Y) and z+k in range(0,Z) and w+l in range(0,W) and (not (i,j,k,l) == (0,0,0,0)):
                        adj_states.append(hypercubes[w+l][z+k][y+j][x+i])
    return adj_states

# alters one particular hypercube
def alter_hypercube(x,y,z,w):
    hypercube = hypercubes[w][z][y][x]
    adj_states = get_adj(x,y,z,w)
    # hypercube active:
    if hypercube in ['#', 'A']:
        # if number of active neighbours is NOT exactly 2 or 3
        if not len([state for state in adj_states if state in ['#', 'A']]) in [2,3]:
            # hypercube is flagged to become inactive
            hypercubes[w][z][y][x] = 'A'
    elif hypercube in ['.', 'I']:
        # if exactly 3 neighbours are active
        if len([state for state in adj_states if state in ['#', 'A']]) == 3:
            # hypercube is flagged to become active
            hypercubes[w][z][y][x] = 'I'

# now let's do thing
# just gonna display the step
step = 0
# and the number of hypercubes active
active_hypercubes = len([hypercube for space in hypercubes for plane in space for row in plane for hypercube in row if hypercube == '#'])
print('started with ' + str(active_hypercubes) + ' active hypercubes.')

while step < 6:
    # start boot cycle
    # get environment and new dimensions
    hypercubes = add_environment(hypercubes)
    W = len(hypercubes) # number of spaces in a hyperspace
    Z = len(hypercubes[0]) # number of planes in a space
    Y = len(hypercubes[0][0]) # number of rows in a plane
    X = len(hypercubes[0][0][0]) # number of hypercubes in a row

    # a hypercube is hypercubes[][][][]
    for w in range(0,W):
        for z in range(0,Z):
            for y in range(0,Y):
                for x in range(0,X):
                    alter_hypercube(x,y,z,w)

    # after this ends, we need to change I to # and A to .
    for w in range(0,W):
        for z in range(0,Z):
            for y in range(0,Y):
                for x in range(0,X):
                    if hypercubes[w][z][y][x] == 'I':
                        hypercubes[w][z][y][x] = '#'
                    elif hypercubes[w][z][y][x] == 'A':
                        hypercubes[w][z][y][x] = '.'
    step += 1
    active_hypercubes = len([hypercube for space in hypercubes for plane in space for row in plane for hypercube in row if hypercube == '#'])

    print('done ' + str(step) + ' boot cycle(s) - we have ' + str(active_hypercubes) + ' active hypercubes')