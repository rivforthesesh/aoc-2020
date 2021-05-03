# construct map now

import numpy

# input
with open('20.txt', 'r') as file:
    input = file.read()

# turn the input into a list
input_list = list(input.split('\n'))

# get a dict of tiles
tiles = {}

# go through the lines
while len(input_list) > 0:
    # grab the tile ID
    tile_str = input_list.pop(0)
    tile_key = int(tile_str.replace('Tile ','').replace(':',''))
    tile_val = []
    # add in rows until we hit a line break
    while len(input_list[0]) > 0:
        row = input_list.pop(0)
        tile_val.append(list(row))
    # we hit a line break
    tile = numpy.array(tile_val)
    tiles[tile_key] = tile
    # skip over this line break
    input_list.pop(0)

# tile[i][j]: i increases going right, j increases going downwards
# tile.shape = (a,b) where a is the number of rows, b the number of columns

# functions to use

# get all 8 bois in d4 (i.e. all possible pieces when applying rotations and reflections) from key
def d4(tile_key):
    tile = tiles[tile_key]
    # start from the base: the tile, and the tile flipped horizontally
    ttiles = [tile, numpy.fliplr(tile)]
    all_d4 = []
    # add all rotations
    for i in range(0,4):
        for ttile in ttiles:
            all_d4.append(numpy.rot90(ttile,i))
    return all_d4 # list of arrays
    # note all_d4[0] is the original tile

# get borders of a tile from tile
def borders(tile_key,variation):
    ttile = d4(tile_key)[variation]
    (rows,cols) = ttile.shape
    top = ttile[0,:]
    bottom = ttile[rows-1,:]
    left = ttile[:,0]
    right = ttile[:,cols-1]
    return {'top': top, 'bottom': bottom, 'left': left, 'right': right}

# get tile keys
unplaced_tiles = [tile_key for tile_key in tiles.keys()]

# puzzle is a list [n,x,y] where n is a tile key and x,y are the coordinates of it
puzzle = []
# start off with one tile
tile_key = unplaced_tiles.pop(0)
puzzle.append([tile_key, 0, 0])

# get possible positions for next tile
def next_tile_pos(puzzle):
    positions_done = [(tile[1],tile[2]) for tile in puzzle]
    adj_positions = []
    offsets = [(1,0),(-1,0),(0,1),(0,-1)]
    for pos in positions_done:
        for offset in offsets:
            adj_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if not adj_pos in positions_done + adj_positions:
                adj_positions.append(adj_pos)
    return adj_positions

# while there are still unplaced tiles
while unplaced_tiles:
    adj_positions = next_tile_pos(puzzle)
    # go through each tile
    for tile_key in unplaced_tiles:
        # get all versions of this tile (with rotation + reflection)
        ttiles = d4(tile_key)
        # go through each possible position
        for pos in adj_positions:
            # get any puzzle pieces around it
            to_left = [tile[0] for tile in puzzle if (tile[1], tile[2]) == (pos[0] - 1, pos[1])]
            to_right = [tile[0] for tile in puzzle if (tile[1], tile[2]) == (pos[0] + 1, pos[1])]
            to_top = [tile[0] for tile in puzzle if (tile[1], tile[2]) == (pos[0], pos[1] - 1)]
            to_bottom = [tile[0] for tile in puzzle if (tile[1], tile[2]) == (pos[0], pos[1] + 1)]
            # get rules needed for a tile going in pos
            border_rules = {}
            if to_left:
                adj_tile_key = to_left[0]
                adj_tile_val = tiles[adj_tile_key]
                border_rules['left'] = borders(adj_tile_key,0)['right']
            if to_right:
                adj_tile_key = to_right[0]
                adj_tile_val = tiles[adj_tile_key]
                border_rules['right'] = borders(adj_tile_key,0)['left']
            if to_top:
                adj_tile_key = to_top[0]
                adj_tile_val = tiles[adj_tile_key]
                border_rules['top'] = borders(adj_tile_key,0)['bottom']
            if to_bottom:
                adj_tile_key = to_bottom[0]
                adj_tile_val = tiles[adj_tile_key]
                border_rules['bottom'] = borders(adj_tile_key,0)['top']
            # go through each possible version of the tile
            for i in range(0,8):
                ttile = ttiles[i]
                ttile_borders = borders(tile_key,i)
                # see if all of the border rules are satisfied
                for direction in border_rules.keys():
                    if not numpy.array_equal(ttile_borders[direction], border_rules[direction]):
                        # does not satify the rule!
                        break # next ttile
                else:
                    # satisfies all rules
                    # we want to replace tile by ttile
                    tiles[tile_key] = ttile
                    # we also want to place this tile_key in the position
                    puzzle.append([tile_key, pos[0], pos[1]])
                    # and we want to remove this tile_key from unplaced_tiles
                    unplaced_tiles.remove(tile_key)
                    break # next pos
    print('tiles placed:', len(tiles.keys()) - len(unplaced_tiles), '     ', end='\r', flush=True)

# get range of x and y coordinates
x_vals = [puzzle_tile[1] for puzzle_tile in puzzle]
y_vals = [puzzle_tile[2] for puzzle_tile in puzzle]
# get max and min coordinates
max_x = max(x_vals)
max_y = max(y_vals)
min_x = min(x_vals)
min_y = min(y_vals)
# get IDs at coordinates
tl = [puzzle_tile[0] for puzzle_tile in puzzle if (puzzle_tile[1],puzzle_tile[2]) == (min_x, min_y)][0]
tr = [puzzle_tile[0] for puzzle_tile in puzzle if (puzzle_tile[1],puzzle_tile[2]) == (max_x, min_y)][0]
bl = [puzzle_tile[0] for puzzle_tile in puzzle if (puzzle_tile[1],puzzle_tile[2]) == (min_x, max_y)][0]
br = [puzzle_tile[0] for puzzle_tile in puzzle if (puzzle_tile[1],puzzle_tile[2]) == (max_x, max_y)][0]
# get product
print('')
print('product of corner tile IDs (part a answer):',tl*tr*bl*br)

# fix coordinates such that min_x = 0 and min_y = 0
puzzle_cc = [] # corrected coordinates
# also put the actual tiles in this list, not the IDs
for puzzle_tile in puzzle:
    tile_id = puzzle_tile[0]
    x = puzzle_tile[1]
    y = puzzle_tile[2]
    puzzle_cc.append([tiles[tile_id], x - min_x, y - min_y])

# set new max values
max_x -= min_x
max_y -= min_y

puzzle = [] # can just clear this
tiles = {} # and also this

# remove borders from each piece
puzzle_nb = [] # no borders
for puzzle_tile in puzzle_cc:
    tile = puzzle_tile[0]
    x = puzzle_tile[1]
    y = puzzle_tile[2]

    # remove border
    tile = tile[1:-1,1:-1]
    puzzle_nb.append([tile, x, y])

puzzle_cc = [] # can just clear this

# [tile,i,j] i increases going right, j increases going down

# append arrays left to right (i.e. same j)
puzzle_rows = [] # row of tiles
for j in range(0,max_y+1):
    row = [tile[0] for tile in puzzle_nb if (tile[1],tile[2]) == (0,j)][0]
    for i in range(1,max_x+1):
        row = numpy.append(row,[tile[0] for tile in puzzle_nb if (tile[1],tile[2]) == (i,j)][0], axis = 1)
    puzzle_rows.append(row)

puzzle_nb = [] # can just clear this

# append rows top to bottom
map = puzzle_rows.pop(0)
while len(puzzle_rows) > 0:
    row = puzzle_rows.pop(0)
    map = numpy.append(map, row, axis = 0)

# get sea monster as array (of '#' and ' ')
sm_str = '                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '
sm = numpy.array([list(line) for line in sm_str.split('\n')])

# get all orientations of sea monster
# altered version of d4
# start from the sea monster and the sea monster flipped
sm_flip = [sm, numpy.fliplr(sm)]
sea_monsters_h = [] # ones where the sea monster is lomg
sea_monsters_v = [] # ones where the sea monster is tol
# add all rotations
for i in range(0,4):
    for smf in sm_flip:
        if i % 2 == 0:
            sea_monsters_h.append(numpy.rot90(smf,i))
        else:
            sea_monsters_v.append(numpy.rot90(smf, i))

# ATTEMPT 1: assume sea monsters do NOT overlap.
# if this gives the wrong answer, then there are overlaps

# return whether the sea monster with that orientation exists here
def find_sea_monster(sea_monster,sm_shape,i,j):
    # get subarray
    sub_map = map[i:i+sm_shape[0], j:j+sm_shape[1]]
    # pattern match
    for x in range(0,sm_shape[0]):
        for y in range(0,sm_shape[1]):
            if sea_monster[x,y] == '#' and not sub_map[x,y] == '#':
                # sea monster is not here
                return False
    # if we get here, then all of these checks passed
    return True

sm_found = 0

# try to find horizontal sea monsters
sm_shape = sea_monsters_h[0].shape
# for every possible coordinate for the top-left of a subarray of this shape
for sea_monster in sea_monsters_h:
    for i in range(0,map.shape[0] - sm_shape[0] + 1):
        for j in range(0,map.shape[1] - sm_shape[1] + 1):
            if find_sea_monster(sea_monster,sm_shape,i,j):
                sm_found += 1

# try to find vertical sea monsters
sm_shape = sea_monsters_v[0].shape
# for every possible coordinate for the top-left of a subarray of this shape
for sea_monster in sea_monsters_v:
    for i in range(0,map.shape[0] - sm_shape[0] + 1):
        for j in range(0,map.shape[1] - sm_shape[1] + 1):
            if find_sea_monster(sea_monster,sm_shape,i,j):
                sm_found += 1

print('sea monsters found:',sm_found)
num_hashes = len([char for char in sm_str if char == '#']) # number of hashes in sea monster
print('sea monsters take up',sm_found*num_hashes,'#s')
map_row_list = map.tolist()
map_elt_list = [elt for row in map_row_list for elt in row]
num_hashes_map = len([char for char in map_elt_list if char == '#'])
print('total number of hashes in map:',num_hashes_map)
print('answer to part b, if no sea monsters overlap:',num_hashes_map - (sm_found*num_hashes))