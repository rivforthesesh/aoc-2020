# add some data validation, quick

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

needed_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
maybe_valid = [] # has all required fields
invalid = [] # missing a required field
for passport in passport_list:
    fields = passport.keys() # list of the fields
    # make sure set of fields contains all needed fields
    if set(needed_fields).issubset(set(fields)): # no cid
        maybe_valid.append(passport)
    else: # invalid
        invalid.append(passport)

print('first problem: ' + str(len(maybe_valid)))

valid = [] # satisfies all the checks
# run validation on each field
for passport in maybe_valid:

    byr = int(passport['byr'])
    if byr < 1920 or byr > 2002:
        invalid.append(passport)
        print('byr ' + str(byr))
        continue

    iyr = int(passport['iyr'])
    if iyr < 2010 or iyr > 2020:
        invalid.append(passport)
        print('iyr ' + str(iyr))
        continue

    eyr = int(passport['eyr'])
    if eyr < 2020 or eyr > 2030:
        invalid.append(passport)
        print('eyr ' + str(eyr))
        continue

    hgt = (passport['hgt'][:-2], passport['hgt'][-2:])
    # e.g. hgt = ('142', 'cm')
    # has to be in or cm, different rules for each
    # ints done later in case it doesn't end cm or in
    if hgt[1] == 'cm':
        if int(hgt[0]) < 150 or int(hgt[0]) > 193:
            invalid.append(passport)
            print('hgt ' + str(hgt))
            continue
    elif hgt[1] == 'in':
        if int(hgt[0]) < 59 or int(hgt[0]) > 76:
            invalid.append(passport)
            print('hgt ' + str(hgt))
            continue
    else: # not cm or in
        invalid.append(passport)
        print('hgt ' + str(hgt))
        continue

    hcl = passport['hcl']
    if hcl[0] == '#': # starts with #
        if len(hcl) == 7: # 6 characters after the #
            for i in range(1,7): # char by char
                # want good letter or int
                if i not in ['a', 'b', 'c', 'd', 'e', 'f']: # if it is not a good letter
                    try: # try to make it an int
                        j = int(i)
                    except: # i is not an int
                        invalid.append(passport)
                        print('hcl ' + str(hcl))
                        continue
    else: # does not start with #
        invalid.append(passport)
        print('hcl ' + str(hcl))
        continue

    ecl = passport['ecl']
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        invalid.append(passport)
        print('ecl ' + str(ecl))
        continue

    pid = passport['pid']
    if len(pid) == 9: # 9 characters
        try:  # try to make it an int
            int_pid = int(pid)
        except:  # pid is not an int
            invalid.append(passport)
            print('pid ' + str(pid))
            continue
    else:
        invalid.append(passport)
        print('pid ' + str(pid))
        continue

    # no continue => all validation checks passed
    valid.append(passport)

print('second problem: ' + str(len(valid)))