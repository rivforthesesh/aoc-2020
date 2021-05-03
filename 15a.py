# numbers memory game

# grab defaultdict so we can have absent keys as a default value
from collections import defaultdict

# input
with open('15.txt', 'r') as file:
    input = file.read()

# it's one line today
# input_list = list(input.split('\n'))

# get num list
num_list = [int(num) for num in input.split(',')]

# start dict
num_dict = defaultdict(int)
# key is a number
# value is the position it was last in
# if key isn't in the dict it's added with default 0

# put starting numbers in dict
i = 0
while i < len(num_list):
    num = num_list[i]
    i += 1
    num_dict[num] = i

# continue down the list
while i < 2020:
    # get the position of the number spoken
    pos = num_dict[num]
    # save new position for current number
    num_dict[num] = i
    # get the next number
    if pos == 0: # number has not come up
        num = 0
    else: # number has come up
        num = i - pos
    i += 1

print(str(i) + '^th number: ' + str(num))