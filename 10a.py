# plugging in adapters
# socket has 0 jolts
# an adapter with n jolts takes >=(n-3) jolts as input, outputs n jolts
# device has a built-in joltage adapter for 3 + max(external adapters)
# what are the 1j and 3j differences if you use all of them?

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

# count number of 1-jolt and 3-jolt differences
j1 = 0
j3 = 0

for i in range(0, len(adapters)-1):
    if adapters[i+1] - adapters[i] == 1:
        j1 += 1
    elif adapters[i+1] - adapters[i] == 3:
        j3 += 1

print(j1 * j3)