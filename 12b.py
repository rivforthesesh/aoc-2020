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

# the ship can be given by two values
# x and y coords
# ABSOLUTE
ship = [0,0]
# waypoint has x and y coords
# this is RELATIVE TO THE SHIP!
waypoint = [1,10]

for inst in instructions:
    dir = inst[0] # move NESW / turn LR / move F
    val = inst[1] # steps or degrees
    # first four are directions
    if dir == 'N':
        waypoint[0] += val
    elif dir == 'E':
        waypoint[1] += val
    elif dir == 'S':
        waypoint[0] -= val
    elif dir == 'W':
        waypoint[1] -= val
    # next two are rotating the waypoint around the ship
    # https://en.wikipedia.org/wiki/Rotation_matrix#Direction
    # i've used x as north/south and y as west/east lol
    elif dir == 'L':
        # a -> ac + bs, b -> -as + bc
        c = int(math.cos(math.radians(val)))
        s = int(math.sin(math.radians(val)))
        a = waypoint[0]
        b = waypoint[1]
        waypoint[0] = a*c + b*s
        waypoint[1] = -a*s + b*c
    elif dir == 'R':
        # a -> ac - bs, b -> as + bc
        c = int(math.cos(math.radians(val)))
        s = int(math.sin(math.radians(val)))
        a = waypoint[0]
        b = waypoint[1]
        waypoint[0] = a*c - b*s
        waypoint[1] = a*s + b*c
    # last one is moving in the direction of the waypoint
    elif dir == 'F':
        ship[0] += val * waypoint[0]
        ship[1] += val * waypoint[1]

print('final position = (' + str(ship[0]) + ', ' + str(ship[1]) + ')')

# calculate manhattan distance
# from (0,0) so we just need final position
md = abs(ship[0]) + abs(ship[1])

print('manhattan distance = ' + str(md))