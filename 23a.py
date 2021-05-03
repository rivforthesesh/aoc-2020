# cups

# input
with open('23.txt', 'r') as file:
    input = file.read()

# it's one line this time
# input_list = list(input.split('\n'))

# grab them cups
cups = [int(c) for c in list(input)]
print(cups)

# function does one pass
# cc is current cup (starts with cups[0])
def grab_cup(cc,cups):

    # get loc of current cup
    # x,y,z are next three cups
    # update cloc in case we wrap around the list
    cloc = cups.index(cc)
    x = cups.pop((cloc+1) % len(cups))
    cloc = cups.index(cc)
    y = cups.pop((cloc+1) % len(cups))
    cloc = cups.index(cc)
    z = cups.pop((cloc+1) % len(cups))
    # cups with value under the current one
    under_cc = [c for c in cups if c < cc]
    if under_cc: # there exists a cup with value < cc
        # destination cup is the max available under cc
        dc = max(under_cc)
    else: # there is no cup with value < cc
        # destination cup is the max available that is not cc
        dc = max([c for c in cups if not c == cc])
    # find location of dc
    dloc = cups.index(dc)
    # place x,y,z
        # list.insert(i, elem)
        # Here, elem is inserted to the list at the ith index.
        # All the elements after elem are shifted to the right.
    cups.insert(dloc+1,z)
    cups.insert(dloc+1,y)
    cups.insert(dloc+1,x)
    # get loc of current cup (might have changed)
    cloc = cups.index(cc)
    # return next cup
    # modulo is to ensure we don't get errors
    print(cups,'cc',cc,'x',x,'y',y,'z',z,'dc',dc)
    return cups[(cloc+1) % len(cups)]

# get first current cup
cc = cups[0]
# and num steps done
i = 0

# run 100 moves
while i < 100:
    cc = grab_cup(cc,cups)
    i += 1

# fix list so 1 is the first
while not cups[0] == 1:
    w = cups.pop(0)
    cups.append(w)
# remove the 1
cups.pop(0)

print('part a answer: ',''.join([str(c) for c in cups]))