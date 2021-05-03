# Starting at the top-left corner of your map and following a slope of right 3 and down 1,
# how many trees would you encounter?
# the same pattern repeats to the right many times

import functools # reduce()
import operator

# input
with open('3.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each row is '..##.......' where # is a tree
input_list = list(input.split('\n'))

row_len = 31 # all rows have the same length in a
dxy_list = [(1,1), (3,1), (5,1), (7,1), (1,2)]
tree_list = [] # will have number of trees
for dx_dy in dxy_list:
    x = 0  # this is where you are in the row
    y = 0  # this is the number row you're on
    dx = dx_dy[0] # this is how many you go right
    dy = dx_dy[1] # this is how many you go down
    num_trees = 0  # counter for number of trees
    while y < len(input_list):
        if input_list[y][x] == '#':
            num_trees += 1
        x = (x + dx) % row_len
        y = y + dy
    # we now have number of trees
    tree_list.append(num_trees)

# we now have the full list
prod_trees = functools.reduce(operator.mul, tree_list)
print(prod_trees)
