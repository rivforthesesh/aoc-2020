# plugging in adapters
# socket has 0 jolts
# an adapter with n jolts takes >=(n-3) jolts as input, outputs n jolts
# device has a built-in joltage adapter for 3 + max(external adapters)
# how many legal arrangements are there?

# input
with open('10.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one number as a string
input_list = list(input.split('\n'))
# get a list of numbers instead of strings
# append on socket joltage
# append on device joltage
# sort
adapters = [int(n) for n in input_list]
adapters.append(0)
adapters.append(max(adapters) + 3)
adapters.sort()

# look at the list of vital adapters
# (socket, device, or either side of a break of 3)
vital_adapters = []
vital_adapters.append(0)
for i in range(0, len(adapters)-1):
    if adapters[i+1] - adapters[i] == 3:
        # either side of a break of 3, and hasn't been added already
        if not i in vital_adapters:
            vital_adapters.append(i)
        if not i+1 in vital_adapters:
            vital_adapters.append(i+1)

# naively getting all legal arrangements of a string of non-vitals
# between two vitals a and b
def nv(nab: int):
    if nab < 0:
        return 1
    elif nab == 0:
        return 1
    elif nab == 1:
        return 2
    elif nab == 2:
        return 4
    else: # cannot jump directly, but can go to 1, 2, or 3 away
        return nv(nab - 1) + nv(nab - 2) + nv(nab - 3)

num_arrangements = 1 # start off by assuming the only arrangement is using all adapters
for j in range(0,len(vital_adapters)-1): # for every vital adapter with a vital adapter after it
    # print(num_arrangements)
    # find maximum number of adapters between this vital adapter and the next
    # nab = number adapters between
    # (the -1 ensures that the next vital adapter is excluded)
    nab = vital_adapters[j+1] - vital_adapters[j] - 1
    # followed by a (possibly empty) string of non-vitals
    # nab=0 => adapters[vital_adapters[j]] is right before a vital adapter
    # need to check how many possible arrangements there are
    # no jumps of 2, so these will all be 1 apart
    num_arrangements = num_arrangements * nv(nab)
    # for debugging:
    #print('\nbetween adapters at pos ' + str(vital_adapters[j]) + ' and ' + str(vital_adapters[j+1]))
    #print('(with joltage ' + str(adapters[vital_adapters[j]]) + ' and ' + str(adapters[vital_adapters[j+1]]) + ')')
    #print(str(adapters[vital_adapters[j]:vital_adapters[j+1]+1]))
    #print('we have this many non-vitals in between: ' + str(nab))
    #print('which has this many arrangements: ' + str(nv(nab)))

# show vital adapters:
#print([adapters[i] for i in vital_adapters])
print(num_arrangements)