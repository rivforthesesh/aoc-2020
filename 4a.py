# Passport data is validated in batch files (your puzzle input).
# Each passport is represented as a sequence of key:value pairs separated by spaces or newlines.
# Passports are separated by blank lines.
# need to have byr, iyr, eyr, hgt, hcl, ecl, pid
# has cid => passport
# does not have cid => north pole credentials (npc)
# ^ treat each of these two as valid

# input
with open('4.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each row is '..##.......' where # is a tree
input_list = list(input.split('\n\n'))

# it can be split by spaces or line breaks
# change line breaks to spaces, then split on spaces
# make these tuples where each entry is like 'eyr:2026'
# then turn these into dicts
passport_list = []
for passport_str in input_list:
    passport_tuple = passport_str.replace('\n', ' ').split(' ')
    passport_dict = {}
    for field in passport_tuple: # of the form 'eyr:2026'
        key_val = field.split(':') # ('eyr', '2026')
        passport_dict[key_val[0]] = key_val[1] # {..., 'eyr':'2026', ...}
    passport_list.append(passport_dict)

# using these:
needed_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
optional_fields = ['cid']
# split passports into these three categories:
valid_pass = [] # valid passport (all needed, all optional)
valid_npc = [] # valid north pole credentials (all needed, no optional)
invalid_pn = [] # invalid as either (not all needed)
for passport in passport_list:
    fields = passport.keys() # list of the fields
    # make sure set of fields contains all needed fields
    if set(fields) == set(needed_fields): # no cid
        valid_npc.append(passport)
    elif set(fields) == set(needed_fields + optional_fields): # has cid
        valid_pass.append(passport)
    else: # invalid
        invalid_pn.append(passport)

print(len(valid_pass) + len(valid_npc))