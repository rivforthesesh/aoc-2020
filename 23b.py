# cups

# for timing
import time

# input
with open('23.txt', 'r') as file:
    input = file.read()

# it's one line this time
# input_list = list(input.split('\n'))

# grab them cups
cups_list = [int(c) for c in list(input)]
# add on mORE CUPS
cups_list = cups_list + [i for i in range(10,1000001)]

# turn it into a dict containing the next value
cups = {}
for i in range(0,len(cups_list)):
    cups[cups_list[i]] = cups_list[(i+1) % len(cups_list)]

# get first current cup
cc = cups_list[0]
del cups_list
# and num steps done
i = 0

# function does one pass
# cc is current cup
def grab_cup(cc):
    # x,y,z are next three cups
    x = cups[cc]
    y = cups[x]
    z = cups[y]
    # get dc
    dc = cc - 1
    while dc in [x,y,z]:
        dc -= 1
    # gone too low if 0
    if dc == 0:
        # go to max
        dc = 1000000
        # work down if needed
        while dc in [x, y, z]:
            dc -= 1
    # place x,y,z by updating next elts
    # ... cc, x, y, z, a ... -> ... cc, a ...
    # ... dc, b ... -> ... dc, x, y, z, b ...
    # get a and b
    a = cups[z]
    b = cups[dc]
    # set new nexts for cc, dc, z (unchanged for x,y,a,b)
    cups[cc] = a
    cups[dc] = x
    cups[z] = b
    # return next cup
    return cups[cc]

tic = time.perf_counter()

# run 100 moves
while i < 10000000:
    cc = grab_cup(cc)
    i += 1
    toc = time.perf_counter()
    print('moves remaining:',10000000-i,'mins elapsed:',int((toc-tic)/60),'mins left:',int(((toc-tic)/i)*(10000000-i)/60),'           ',end = '\r', flush = True)

# get the two cups after 1
p = cups[1]
q = cups[p]

print('part b answer: ',p * q,'                          ')
print('seconds taken:',toc-tic)

# 182793916466