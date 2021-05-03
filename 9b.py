# XMAS starts by transmitting a preamble of 25 numbers.
# After that, each number you receive should be the sum of any two of the 25 immediately previous numbers.
# The two numbers will have different values, and there might be more than one such pair.

# input
with open('9.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one number as a string
input_list = list(input.split('\n'))
# get a list of numbers instead of strings
num_list = [int(n) for n in input_list]
# keep a list of the previous 25 numbers
tf = []

for n in num_list:
    # first 25 numbers case
    if len(tf) < 25: # in preamble
        tf.append(n) # add to list
        continue # go to next num

    # after first 25 numbers case
    # for int pairs (i,j) where 0 <= i < j < 25
    for i in range(0,24):
        for j in range(i+1,25):
            if not tf[i] == tf[j]: # numbers must have distinct values
                if tf[i] + tf[j] == n: # must add up to n
                    break # tf[i] =/= tf[j] and tf[i] + tf[j] = n
        else:
            # j loop did not break
            # there is no such j; go to next i
            continue
        # j loop broke
        # tf[i] =/= tf[j] and tf[i] + tf[j] = n
        break
    else:
        # i loop did not break
        # => j loop did not break
        # => invalid number
        print('invalid number (part a): ' + str(n))
        # we have the answer
        break # n loop

    # if we get here, then we are past preamble and had a valid number
    # remove first number from tf
    tf.pop(0)
    # add latest number to tf
    tf.append(n)

# part b time
# must find a contiguous set of at least two numbers in your list
# which sum to the invalid number from step 1
# To find the encryption weakness, add together the smallest and largest number in this contiguous range

# get a list of consecutive numbers
cs = []

# checked: every number in the list is positive
for m in num_list:
    # add m to the list
    cs.append(m)
    # make sure the sum is <= n
    while sum(cs) > n:
        # too large; remove first number
        cs.pop(0)
    # check if list is at least len 2
    if len(cs) > 1:
        if sum(cs) == n: # if it adds up to n
            print('encryption weakness (part b): ' + str(min(cs) + max(cs)))
            break # we have the answer
        else: # sum(cs) < n
            continue # need to append the next
    else:
        continue # only one so we need to append the next