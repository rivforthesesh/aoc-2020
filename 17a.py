# cellular automata but with cubes
# how many are active at 6th boot cycle?

# input
with open('17.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one row of cubes
input_list = list(input.split('\n'))

# turn each row into a list, so cube_start has a list of lists
# (cube_start is a plane)
cube_start = [list(row) for row in input_list]

# one more dimension to get the space
cubes = [cube_start]
# [[['#', '.', '.', '.', '.', '#', '.', '#'],
#   ['.', '.', '#', '#', '.', '#', '#', '.'],
#   ['#', '.', '.', '#', '.', '.', '#', '.'],
#   ['.', '#', '.', '.', '#', '.', '.', '#'],
#   ['.', '#', '.', '.', '#', '.', '.', '.'],
#   ['#', '#', '.', '#', '#', '#', '#', '#'],
#   ['#', '.', '.', '#', '.', '.', '#', '.'],
#   ['#', '#', '.', '#', '#', '.', '.', '#']]]

# states given:
# active = #
# inactive = .

# to avoid deep copies, i'm going to introduce two more states:
# I = currently inactive, will become active
# A = currently active, will become inactive

# CA rules:
# active + number of active next to it is NOT 2 or 3 => inactive
# inactive + three active next to it => active

#for y in range(0, len(cubes[0])):
#    print(cubes[0][y])
#print('')

# adds the surrounding environment to the space
# cubes = [...,plane,...]
# plane = [...,row,...]
# row = [...,cube,...]
def add_environment(cubes):
    Z = len(cubes) # number of planes in a space cubes
    Y = len(cubes[0]) # number of rows in a plane cubes[i]
    X = len(cubes[0][0]) # number of cubes in a row cubes[i][j]
    # a cube is cubes[i][j][k]
    # surround each row: one . either side (L and R)
    for z in range(0,Z):
        for y in range(0,Y):
            # cubes[z][y] is a row
            cubes[z][y] = ['.'] + cubes[z][y] + ['.']
    X += 2 # added two more cubes to each row
    # surround each plane: one row of . either side (T and Bo)
    for z in range(0,Z):
        # cubes[z] is a plane
        cubes[z] = [['.']*X] + cubes[z] + [['.']*X]
    Y += 2 # added two more rows to each plane
    # finally, surround the space with two planes of . (F and Ba)
    # cubes = [[['.']*X]*Y] + cubes + [[['.']*X]*Y] # each [['.']*X]*Y references the same ['.']*X Y times
    # [[] for i in range(0,n)]
    # instead of [[]]*n
    cubes = [[['.']*X for y in range(0,Y)]] + cubes + [[['.']*X for y in range(0,Y)]] # each [['.']*X]*Y
    Z += 2
    return cubes

# gets states of adjacent cubes
def get_adj(x,y,z):
    offsets = [-1,0,1]
    adj_states = []
    Z = len(cubes) # number of planes in a space cubes
    Y = len(cubes[0]) # number of rows in a plane cubes[i]
    X = len(cubes[0][0]) # number of cubes in a row cubes[i][j]
    for i in offsets:
        for j in offsets:
            for k in offsets:
                # if in range (note: will be done after adding environment)
                if x+i in range(0,X) and y+j in range(0,Y) and z+k in range(0,Z) and (not (i,j,k) == (0,0,0)):
                    adj_states.append(cubes[z+k][y+j][x+i])
    return adj_states

# alters one particular cube
def alter_cube(x,y,z):
    cube = cubes[z][y][x]
    adj_states = get_adj(x,y,z)
    # cube active:
    if cube in ['#', 'A']:
        # if number of active neighbours is NOT exactly 2 or 3
        if not len([state for state in adj_states if state in ['#', 'A']]) in [2,3]:
            # cube is flagged to become inactive
            cubes[z][y][x] = 'A'
    elif cube in ['.', 'I']:
        # if exactly 3 neighbours are active
        if len([state for state in adj_states if state in ['#', 'A']]) == 3:
            # cube is flagged to become active
            cubes[z][y][x] = 'I'
            # print('set a cube with ' + str(len([state for state in adj_states if state in ['#', 'A']]))+ ' active neighbours to ' + cubes[z][y][x])

# now let's do thing
# just gonna display the step
step = 0
# and the number of cubes active
active_cubes = len([cube for row in cube_start for cube in row if cube == '#'])
print('started with ' + str(active_cubes) + ' active cubes.')

while step < 6:
    # start boot cycle
    # get environment and new dimensions
    cubes = add_environment(cubes)
    Z = len(cubes)  # number of planes in a space cubes
    Y = len(cubes[0])  # number of rows in a plane cubes[i]
    X = len(cubes[0][0])  # number of cubes in a row cubes[i][j]

    # print boi
    #for z in range(0, Z):
    #    for y in range(0, Y):
    #        print(cubes[z][y])
    #    print('')
    #print('dimensions:', X, Y, Z)

    # a cube is cubes[i][j][k]
    for z in range(0, Z):
        for y in range(0, Y):
            for x in range(0, X):
                alter_cube(x, y, z)

    # after this ends, we need to change I to # and A to .
    for z in range(0, Z):
        for y in range(0, Y):
            for x in range(0, X):
                if cubes[z][y][x] == 'I':
                    cubes[z][y][x] = '#'
                elif cubes[z][y][x] == 'A':
                    cubes[z][y][x] = '.'
    step += 1
    active_cubes = len([cube for plane in cubes for row in plane for cube in row if cube == '#'])

    print('done ' + str(step) + ' boot cycle(s) - we have ' + str(active_cubes) + ' active cubes')