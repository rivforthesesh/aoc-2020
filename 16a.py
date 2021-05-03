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

print(error_rate)
# not 983