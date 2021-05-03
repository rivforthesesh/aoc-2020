# this airline uses binary space partitioning to seat people.
# A seat might be specified like FBFBBFFRLR, where
# F means "front", B means "back", L means "left", and R means "right"
# F/L lower half, B/R upper half
# What is the highest seat ID on a boarding pass?

# input
with open('5.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each row is a string FBFBBFFRLR
input_list = list(input.split('\n'))

# find largest
big_num = 0 # highest seat ID so far
for seat in input_list:
    # convert to a binary string
    seat_bin = ''
    for i in range(0,len(seat)):
        if seat[i] in ('F', 'L'):
            seat_bin = seat_bin + '0'
        elif seat[i] in ('B', 'R'):
            seat_bin = seat_bin + '1'
    # convert this to an int
    num = int(seat_bin, 2)
    # keep iff it is larger than all ones so far
    if num > big_num:
        big_num = num

print(big_num)