# turtle boi but with a ship
# what is the manhattan distance from the start (0,0)?

# get sin and cos
import math

# input
with open('12.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one instruction
input_list = list(input.split('\n'))
# split into letter and number
instructions = [(str[0], int(str[1:])) for str in input_list]
# 'F10' -> ('F', 10)

# the ship (turtle) can be given by three values
# direction it's facing (as a bearing from north)
# (or vaguely as a bearing lol, cba to put it between 0 and 359
# so 0 => N, 90 => E, 180 => S, 270 => W
# x and y coords
turtle = [90,0,0]

for inst in instructions:
    dir = inst[0] # move NESW / turn LR / move F
    val = inst[1] # steps or degrees
    # first four are directions
    if dir == 'N':
        turtle[1] += val
    elif dir == 'E':
        turtle[2] += val
    elif dir == 'S':
        turtle[1] -= val
    elif dir == 'W':
        turtle[2] -= val
    # next two are turns
    elif dir == 'L':
        turtle[0] -= val
    elif dir == 'R':
        turtle[0] += val
    # last one is walking forward
    elif dir == 'F':
        # get the direction we're facing in degrees
        deg = turtle[0]
        # might as well over engineer
        # remember math.cos/sin take radians as an argument
        # math.radians converts deg -> rad
        # math.cos takes the cosine
        # int rounds to the nearest integer bc rounding point errors
        # (so this version only works with right angles)
        turtle[1] += val * int(math.cos(math.radians(deg)))
        turtle[2] += val * int(math.sin(math.radians(deg)))

print('final angle = ' + str(turtle[0]))
print('final position = (' + str(turtle[1]) + ', ' + str(turtle[2]) + ')')

# calculate manhattan distance
# from (0,0) so we just need final position
md = abs(turtle[1]) + abs(turtle[2])

print('manhattan distance = ' + str(md))