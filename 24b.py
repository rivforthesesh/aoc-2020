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

# checks if two complex numbers a and b are the same tile
def is_same_tile(a, b):
    # close enough real parts
    if isclose(a.real, b.real, rel_tol=10 ** -10, abs_tol=10 ** -10):
        # close enough imag parts
        if isclose(a.imag, b.imag, rel_tol=10 ** -10, abs_tol=10 ** -10):
            return True
    return False

# count flips per tile
tiles = {}
for tile_flip in tile_flips:
    # check if tile is already in tiles
    for tile in tiles.keys():
        if is_same_tile(tile,tile_flip):
            # add another flip
            tiles[tile] = tiles[tile] + 1
            break # next tile_flip
    else:
        # tile is not already in tiles
        tiles[tile_flip] = 1

# black side up <=> number of flips is odd
print('part a answer:',len([num for num in tiles.values() if num % 2 == 1]))

# add tile environment (so the surrounding tiles are all white)
def get_environment():
    tiles_to_add = []
    # throw in adjacents of each tile (that are not already done)
    for tile in tiles.keys():
        for k in range(0,6):
            a_tile = tile + z**k
            for b_tile in tiles.keys():
                if is_same_tile(a_tile,b_tile):
                    break # already done; break b_tile. next k
            else:
                # if we get here there was no break
                # check if this one has already been put into consideration
                for c_tile in tiles_to_add:
                    if is_same_tile(a_tile, c_tile):
                        break  # already done; break c_tile. next k
                else:
                    # if we get here this didn't break either
                    tiles_to_add.append(a_tile)
    # now we throw in all the new tiles
    while tiles_to_add:
        tiles[tiles_to_add.pop(0)] = 0

# now to work this into part b
# tiles has all of the tiles currently being considered (all other tiles are white)
# remove all white tiles at the end of the day for memory
def day_pass():
    # get list of tiles to flip
    tiles_to_flip = []
    # go through each tile
    for tile in tiles.keys():
        # get number of surrounding tiles that are black
        adj_black = 0
        # for each direction
        for k in range(0,6):
            # get the adjacent tile in that direction
            a_tile = tile + z**k
            # check if tile is the same as any in tiles.keys()
            for b_tile in tiles.keys():
                if is_same_tile(a_tile,b_tile):
                    # check if tile is black
                    if tiles[b_tile] % 2 == 1:
                        adj_black += 1
            # tile not in tiles.keys() => tile is black
        # we now have the number of adjacent black tiles
        if tiles[tile] % 2 == 0: # current tile is white
            if adj_black == 2: # 2 black tiles adjacent
                tiles_to_flip.append(tile)
        else: # current tile is black
            if adj_black == 0 or adj_black > 2: # 0 or 3+ black tiles adjacent
                tiles_to_flip.append(tile)
    # flip these tiles
    while tiles_to_flip:
        tile = tiles_to_flip.pop(0)
        tiles[tile] = tiles[tile] + 1
    # remove white tiles
    white_tiles = []
    for tile in tiles.keys():
        if tiles[tile] % 2 == 0:
            white_tiles.append(tile)
    for tile in white_tiles:
        del tiles[tile]

# run 100 days
for i in range(0,100):
    get_environment()
    print('running day',i+1,'with',len(tiles.keys()),'tiles...')
    day_pass()

# black side up <=> number of flips is odd
print('part b answer:',len([num for num in tiles.values() if num % 2 == 1]))