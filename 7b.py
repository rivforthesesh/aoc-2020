# many rules (your puzzle input) are being enforced about bags and their contents;
# bags must be color-coded and must contain specific quantities of other color-coded bags
# You have a shiny gold bag. How many bags go inside this bag?

# grab defaultdict so we can have absent keys as empty lists []
from collections import defaultdict

# input
with open('7.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one rule
input_list = list(input.split('\n'))

# make an empty defaultdict to contain e.g. 'light olive' : [(2, 'drab blue'), (1, 'plaid purple')]
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

# get the number of bags inside your current bag
# recursion all the way down
def num_bags_inside(col: str):
    bags_inside = rules[col]
    num = 0
    if bags_inside == []: # no bags inside
        return num
    else: # bags inside
        for numcol in bags_inside:
            # numcol = (2, 'mirrored blue')
            num += numcol[0] + numcol[0] * num_bags_inside(numcol[1])
    return num
# shiny gold bags contain 2 mirrored blue bags, 1 muted brown bag, 3 dim purple bags.
# numcols = [(2, 'mirrored blue'), (1, 'muted brown'), (3, 'dim purple')]

print(num_bags_inside('shiny gold'))