# cellular automata but with plane seats
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
# empty + no occupied next to it => occupied
# occupied + four or more occupied next to it => empty

# get adjacent seats (removing ones with coords out of range)
def get_adj(i: int, j: int):
    adj_seats = []
    for ia in [i-1, i, i+1]:
        for ja in [j-1, j, j+1]:
            if (ia >= 0 and ia < row_len) and (ja >= 0 and ja < num_row): # in range
                if not (ia == i and ja == j): # and not the middle seat
                    adj_seats.append(plane_seats[ja][ia])
    return adj_seats

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
            # get states of adjacent seats
            adj_seats = get_adj(i,j)

            # L = currently empty, next state undetermined
            # # = currently occupied, next state undetermined
            # E = currently empty, will become occupied
            # O = currently occupied, will become empty

            # empty + no occupied next to it => occupied
            if seat in ['L', 'E']:
                if not ('#' in adj_seats or 'O' in adj_seats):
                    plane_seats[j][i] = 'E'
                    has_changed = True
            # occupied + four or more occupied next to it => empty
            if seat in ['#', 'O']:
                occ = 0
                for adj_seat in adj_seats:
                    if adj_seat in ['#', 'O']:
                        occ += 1
                    if occ == 4:
                        plane_seats[j][i] = 'O'
                        has_changed = True
                        break
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

print('(part a) final number of seats occupied: ' + str(num_occ) + ' of ' + str(num_seats))