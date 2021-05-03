# Starting at the top-left corner of your map and following a slope of right 3 and down 1,
# how many trees would you encounter?
# the same pattern repeats to the right many times

# input
with open('3.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each row is '..##.......' where # is a tree
input_list = list(input.split('\n'))

xpos = 0 # this is where you are in the row
row_len = 31 # all rows have the same length in a
num_trees = 0 # counter for number of trees
for row in input_list:
    try:
        if row[xpos] == '#':
            num_trees += 1
    except:
        print('row: ' + row)
        print('xpos = ' + str(xpos))
        print('num_trees = ' + str(num_trees))
    xpos = (xpos + 3) % row_len

print(num_trees)
