# this airline uses binary space partitioning to seat people.
# A seat might be specified like FBFBBFFRLR, where
# F means "front", B means "back", L means "left", and R means "right"
# F/L lower half, B/R upper half
# What is your seat ID?

# input
with open('5.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each row is a string FBFBBFFRLR
input_list = list(input.split('\n'))

# get a list of all seat IDs
seats = []
for seat_str in input_list:
    # convert to a binary string
    seat_bin = ''
    for i in range(0,len(seat_str)):
        if seat_str[i] in ('F', 'L'):
            seat_bin = seat_bin + '0'
        elif seat_str[i] in ('B', 'R'):
            seat_bin = seat_bin + '1'
    # convert this to an int
    seat = int(seat_bin, 2)
    # add to list of seats
    seats.append(seat)

# sort list
seats.sort()

# find two consecutive seats with a difference of 2
for i in range(0, len(seats)):
    if seats[i+1] - seats[i] == 2:
        print(seats[i] + 1)
        break # found the answer