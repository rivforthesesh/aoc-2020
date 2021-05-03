# puzzle

# wooo first time
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

# get range of x coordinates
x_vals = [puzzle_tile[1] for puzzle_tile in puzzle]
y_vals = [puzzle_tile[2] for puzzle_tile in puzzle]
# get max and min
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