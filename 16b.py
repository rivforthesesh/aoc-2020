# input
with open('16.txt', 'r') as file:
    input = file.read()

# reading in tickets
input_list = list(input.split('\n'))

# start iterating over lines
line_no = 0
line = input_list[line_no]

# get the rules as a list of dicts
rules = []
while len(line) > 0: # before the blank line
    # departure location: 31-538 or 546-960
    line1 = line.split(': ')
    # ['departure location', '31-538 or 546-960']
    line2 = [line1[0],] + line1[1].split(' or ')
    # ['departure location', '31-538', '546-960']
    line3 = [line2[0],] + line2[1].split('-') + line2[2].split('-')
    # ['departure location', '31', '538', '546', '960']
    line4 = [line3[0],] + [int(num) for num in line3[1:]]
    # ['departure location', 31, 538, 546, 960]
    rules.append(line4)
    # next line
    line_no += 1
    line = input_list[line_no]

# current line is empty
# skip 'your ticket:'
line_no += 2
line = input_list[line_no]
my_ticket = [int(num) for num in line.split(',')]

# skip empty line, 'nearby tickets:'
line_no += 3
line = input_list[line_no]
tickets = []
while line_no < len(input_list):
    line = input_list[line_no]
    tickets.append([int(num) for num in line.split(',')])
    line_no += 1

# part a flatten time
# gives a list of all the fields
all_tickets = [num for ticket in tickets for num in ticket]
# get confirmed_valid and confirmed_invalid lists for speedy
confirmed_valid = []
confirmed_invalid = []
# error rate for output
error_rate = 0

# check all fields
for num in all_tickets:
    # print('checking number: ' + str(num), end = '\r', flush = True)
    # check if already in/valid
    if num in confirmed_valid:
        continue # go to next field
    elif num in confirmed_invalid:
        error_rate += num # add error
        continue # go to next field
    # new num!
    for rule in rules:
        # rule = ['departure location', 31, 538, 546, 960]
        # check if this value is valid for this field
        if (rule[1] <= num <= rule[2]) or (rule[3] <= num <= rule[4]):
            # value is valid!
            confirmed_valid.append(num)
            break
    else:
        # did not break
        confirmed_invalid.append(num)
        error_rate += num

print('error rate (part a):' + str(error_rate))

# remove all invalid tickets
invalid_tickets = []
for ticket in tickets:
    for num in ticket:
        if num in confirmed_invalid:
            invalid_tickets.append(ticket)
            break
for ticket in invalid_tickets:
    tickets.remove(ticket)

# list of all possible combos
ticket_len = len(my_ticket)
loc_to_field = {}
for i in range(0,ticket_len):
    loc_to_field[i] = [j for j in range(0,ticket_len)]
    # i.e. the value in loc i can correspond to field j

# locs where we know the field for them
# i.e. unknown_locs = loc in loc_to_field.keys() if len(loc_to_field[loc]) > 1
unknown_locs = [i for i in range(0,ticket_len)]

# this list of tickets definitely has no invalid tickets (checked)
for ticket in tickets: # get a list of numbers (ticket)
    known_locs = [] # new locations where we know the field
    for i in unknown_locs: # get one of the locs
        num = ticket[i] # value of ticket in loc i
        can_be_field = loc_to_field[i] # possible fields for loc i
        cant_be_field = [loc_to_field[j][0] for j in known_locs] # impossible fields for loc i (found on this check)
        # starts off with the fields attached to known locs
        for j in can_be_field:
            rule = rules[j] # get the rule for this field
            if not ((rule[1] <= num <= rule[2]) or (rule[3] <= num <= rule[4])):
                # does not satisfy rule for this field
                cant_be_field.append(j)
        # we now have a list of fields that it can't be, based on this value
        for j in cant_be_field:
            if j in can_be_field:
                can_be_field.remove(j)
            # rule = rules[j]
            # print('location ' + str(i) + ' cannot be field number ' + str(j) + ': value ' + str(ticket[i]) + ' is outside ranges [' + str(rule[1]) + ',' + str(rule[2]) + '] \cup [' + str(rule[3]) + ',' + str(rule[4]) + ']')
        # update dict
        loc_to_field[i] = can_be_field
        # remove this field as a possibility from all others, if it's the only one left
        if len(can_be_field) == 1:
            #print(can_be_field)
            known_locs.append(i)
    # remove from unknown_locs if it's a known loc
    for i in known_locs:
        unknown_locs.remove(i)
        print('determined field ' + str(loc_to_field[i][0]) + ' for number in loc ' + str(i))

print('gone through all tickets. reducing list of possible values...')
known_locs = [i for i in range(0,ticket_len) if not i in unknown_locs]

# knock down the possible list even further
while unknown_locs: # while there is at least one unknown loc
    for i in unknown_locs: # go through unknown locs
        if len(loc_to_field[i]) == 1: # if this should actually be a known loc
            known_locs.append(i) # add to known locs
            print('determined field ' + str(loc_to_field[i][0]) + ' for number in loc ' + str(i))
        else: # still an unknown loc
            for j in known_locs: # go through known locs
                k = loc_to_field[j][0] # get the field for the known loc
                if i != j and k in loc_to_field[i]:
                    print('removing ' + str(k) + ' from possibilities for loc ' + str(j))
                    # if this is a different loc and has this field
                    # remove the field
                    tmp = loc_to_field[i]
                    tmp.remove(k)
                    loc_to_field[i] = tmp
    # remove known locs from unknown_locs
    for i in known_locs:
        if i in unknown_locs:
            unknown_locs.remove(i)

print(loc_to_field)

# now we have loc_to_field[i] = [j] <=> the i^th number in a ticket is the j^th field

output = 1
for i in range(0,ticket_len):
    rule_num = loc_to_field[i][0]
    rule = rules[rule_num]
    if rule[0][:9] == 'departure':
        output *= my_ticket[i]

print('departure product (part b):' + str(output))

# not 24027204713620234464237576000077017801