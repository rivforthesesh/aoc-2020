# how many seats are occupied in the final state?

# input
with open('11.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one row of seats
input_list = list(input.split('\n'))

# turn each row into a list, so plane_seats has a list of lists
plane_seats = [list(row) for row in input_list]

# get size of array
row_len = len(plane_seats[0]) # row length
num_row = len(plane_seats) # number of rows

# get number of seats
num_seats = 0
for i in range(0, row_len):
    for j in range(0, num_row):
        if plane_seats[j][i] == 'L':
            num_seats += 1

# states given:
# empty = L
# occupied = #
# floor = .

# to avoid deep copies, i'm going to introduce two more states:
# E = currently empty, will become occupied
# O = currently occupied, will become empty

# CA rules:
# empty + sees no occupied => empty
# occupied + sees five occupied => empty

# get list of directions as offset (i,j), i.e. (-1,1) is 1 left 1 down
dirs = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

# get Number of Occupied Visible seats
def get_nov(i: int, j: int):
    nov = 0
    for dir in dirs:
        # get i-offset and j-offset
        io = dir[0]
        jo = dir[1]
        while 1:
            if i + io < 0 or i + io >= row_len or j + jo < 0 or j + jo >= num_row: # not in range
                break # we went too far
            if plane_seats[j + jo][i + io] == '.':
                # the spot in that direction is the floor
                # take another step in that direction
                io += dir[0]
                jo += dir[1]
            elif plane_seats[j + jo][i + io] in ['L', 'E']:
                # the first seat you see is empty
                # go to next dir
                break
            elif plane_seats[j + jo][i + io] in ['#', 'O']:
                # the first seat you see is occupied
                # add one to nov then go to next dir
                nov += 1
                break
    return nov

# just gonna display the step
step = 0
# and the number of seats occupied
num_occ = 0

# loop until no change
while 1:
    # track if a change was made at each step
    has_changed = False

    print('starting step ' + str(step) + '. seats occupied: ' + str(num_occ) + ' of ' + str(num_seats), end='\r', flush=True)
    for i in range(0, row_len):
        for j in range(0, num_row):
            # get state of current seat
            seat = plane_seats[j][i]

            # L = currently empty, next state undetermined
            # # = currently occupied, next state undetermined
            # E = currently empty, will become occupied
            # O = currently occupied, will become empty

            # empty + sees no occupied => occupied
            if seat in ['L', 'E']:
                if get_nov(i,j) == 0:
                    plane_seats[j][i] = 'E'
                    has_changed = True
            # occupied + five or more occupied in vision => empty
            if seat in ['#', 'O']:
                if get_nov(i,j) >= 5:
                    plane_seats[j][i] = 'O'
                    has_changed = True
            # o/w no change
    # if no changes, we are done
    if not has_changed:
        break
    # o/w increase step and move to next stage (E -> #, O -> L)
    step += 1
    for i in range(0, row_len):
        for j in range(0, num_row):
            # get state of current seat
            seat = plane_seats[j][i]
            # see if it should go empty to occupied
            if seat == 'E':
                plane_seats[j][i] = '#'
                num_occ += 1
            # see if it should go occupied to empty
            if seat == 'O':
                plane_seats[j][i] = 'L'
                num_occ -= 1
            # if it's . (floor), L, or #, no change

print('(part b) final number of seats occupied: ' + str(num_occ) + ' of ' + str(num_seats))