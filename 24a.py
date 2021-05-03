# hex

# complex maths
import cmath
# roughly equal
from math import isclose

# input
with open('24.txt', 'r') as file:
    input = file.read()
input_list = list(input.split('\n'))

# sixth roots of unity
# rads: 0, pi/3, 2pi/3, pi, 4pi/3, 5pi/3
phi = cmath.pi / 3
# primitive in (re, im) form
z = cmath.rect(1, phi)

tile_flips = []

# convert lines to sums
# note that i is denoted by 1j
for line in input_list:
    # put +s in between
    # do on a few lines for legibility
    line = line.replace('ne', 'z + ').replace('nw', 'z**2 + ')
    line = line.replace('sw', 'z**4 + ').replace('se', 'z**5 + ')
    # z**0 = 1, z**3 = -1
    line = line.replace('e', '1 + ').replace('w', '(-1) + ')
    # remove last ' + '
    line = line[:-3]
    # evaluate
    tile_flips.append(eval(line))

# count flips per tile
tiles = {}
for tile_flip in tile_flips:
    # check if tile is already in tiles
    for tile in tiles.keys():
        # close enough real parts
        if isclose(tile.real, tile_flip.real, rel_tol = 10**-10, abs_tol = 10**-10):
            # close enough imag parts
            if isclose(tile.imag, tile_flip.imag, rel_tol = 10 ** -10, abs_tol = 10**-10):
                # add another flip
                tiles[tile] = tiles[tile] + 1
                break # next tile_flip
    else:
        # tile is not already in tiles
        tiles[tile_flip] = 1

# black side up <=> number of flips is odd
print('part a answer:',len([num for num in tiles.values() if num % 2 == 1]))

# 211 too low
# 287
# 293 too high