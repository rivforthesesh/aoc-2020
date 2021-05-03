# many rules (your puzzle input) are being enforced about bags and their contents;
# bags must be color-coded and must contain specific quantities of other color-coded bags
# You have a shiny gold bag. If you wanted to carry it in at least one other bag,
# how many different bag colors would be valid for the outermost bag?
# (In other words: how many colors can, eventually, contain at least one shiny gold bag?)

# grab defaultdict so we can have absent keys as empty lists []
from collections import defaultdict

# input
with open('7.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one rule
input_list = list(input.split('\n'))

# make an empty defaultdict to contain e.g. 'light olive' : [(2, 'drab blue'), (1, 'plaid purple')]
# futureproofing bc part 2 will probably involve the numbers
# if a key is missing, the list of bags it contains is []
rules = defaultdict(list)

# need to split up properly
for rule0 in input_list:
    # rule0 = 'light olive bags contain 2 drab blue bags, 1 plaid purple bag.'
    rule1 = rule0[:-1].split(' bags contain ')
    # ('light olive', '2 drab blue bags, 1 plaid purple bag')
    outer_col = rule1[0]
    # 'light olive'
    rule2 = rule1[1].split(', ')
    # ('2 drab blue bags', '1 plaid purple bag')
    numcol_list = []
    for numcol in rule2:
        if numcol == 'no other bags':
            break # nothing to add to numcol_list
        rule3 = numcol.split(' ')
        # ('2', 'drab', 'blue', 'bags')
        rule4 = (int(rule3[0]), rule3[1] + ' ' + rule3[2])
        # (2, 'drab blue')
        numcol_list.append(rule4)
        # [(2, 'drab blue')]
    # rule3 = [(2, 'drab blue'), (1, 'plaid purple')]
    rules[outer_col] = numcol_list
    # { ... 'light olive': [(2, 'drab blue'), (1, 'plaid purple')], ...}

# gets list of all colours of bags in the dict
# ['light chartreuse', 'dotted silver', ...]
cols = list(rules)
# will contain list of colours containing shiny gold
has_shiny_gold = []
# will contain list of colours not containing shiny gold
no_shiny_gold = []

# gets colours the next level down
# 'light olive' -> ['drab blue', 'plaid purple']
def contains_cols(col: str):
    numcols = rules[col]
    cols = []
    for numcol in numcols:
        cols.append(numcol[1])
    return cols

# we will gradually remove colours
while len(cols) > 0:
    outer_col = cols.pop(0) # pop off the first col in the list
    cols_inside = contains_cols(outer_col) # get the cols one level down
    while len(cols_inside) > 0: # while we still have cols inside
        if 'shiny gold' in cols_inside: # if we have shiny gold inside
            has_shiny_gold.append(outer_col) # add to output list
            break
        inner_col = cols_inside.pop(0) # pop first element from list
        if inner_col in no_shiny_gold: # if we've already confirmed it has no shiny gold
            continue # go to next element in list
        elif inner_col in has_shiny_gold: # if we've already confirmed it has a shiny gold
            has_shiny_gold.append(outer_col)  # add to output list
            break # don't need to continue the while
        cols_inside = cols_inside + contains_cols(inner_col) # get the cols inside that
    else:
        # no break statement hit, cols_inside = 0
        # => does not contain shiny gold
        no_shiny_gold.append(outer_col)

print(len(has_shiny_gold))