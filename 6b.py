# The form asks a series of 26 yes-or-no questions marked a through z.
# All you need to do is identify the questions for which everyone in your group answers "yes".

# input
with open('6.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one group
input_list = list(input.split('\n\n'))

# counter for result
count = 0

# within each group
# turn each line into a set of letters
for group in input_list:
    # turn into a list of the string for each member
    memb_strs = group.split('\n')
    # this list will contain sets of questions answered
    memb_sets = []
    for memb_str in memb_strs:
        # get a set of the questions answered
        memb_set = set(list(memb_str))
        # add to list
        memb_sets.append(memb_set)
    # take the intersection over the group
    grp_set = set.intersection(*memb_sets)
    # add the size of this intersection to the count
    count += len(grp_set)

# we now have the sum of sizes of all intersections
print(count)