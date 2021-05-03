# cups

# for timing
import time

# input
with open('23.txt', 'r') as file:
    input = file.read()

# it's one line this time
# input_list = list(input.split('\n'))

# grab them cups
cups = [int(c) for c in list(input)]
print(cups)
# add on mORE CUPS
for i in range(10,1000001):
    cups.append(i)

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
    return cups[(cloc+1) % len(cups)]

# get first current cup
cc = cups[0]
# and num steps done
i = 0

tic = time.perf_counter()

# run 100 moves
while i < 10000000:
    cc = grab_cup(cc,cups)
    i += 1
    toc = time.perf_counter()
    print('moves remaining:',10000000-i,'mins left:',int(((toc-tic)/i)*(10000000-i)/60),end = '\r', flush = True)

# get the two cups after 1
p = cups[1]
q = cups[p]

print('part b answer: ',p * q,'                          ')