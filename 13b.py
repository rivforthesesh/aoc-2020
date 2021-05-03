# catching the bus
# big boi crt

from functools import reduce
# for floor, gcd
import math
# var 1
# if len(numbers) > 2:
#     return reduce(lambda x,y: GCD([x,y]), numbers)
# var 2 (list is [a,b,c,d])
# gcd = reduce(lambda x,y:GCD([x,y]),[a,b,c,d])

# input
with open('13.txt', 'r') as file:
    input = file.read()

# turn the input into a list - this has when you arrive and the list of buses
input_list = list(input.split('\n'))
# get your buses
buses_str = input_list[1].split(',')
# turn the ones in service into ints and gets the dt we need
buses = []
dt = 0
for bus_str in buses_str:
    if not bus_str == 'x':
        # buses.append((int(bus_str), -dt))
        buses.append((int(bus_str), (-dt) % int(bus_str)))
    dt += 1
print(buses)

# with my input (without doing %) i get this:
# [(29, 0), (37, 23), (631, 29), (13, 47), (19, 48), (23, 52), (383, 60), (41, 70), (17, 77)]
# so my answer is the first n such that all of these are true:
# n % 29 = 0, n % 37 = 23, n % 631 = 29, n % 13 = 47, ..., n % 17 = 77
# the bus numbers are all pairwise distinct primes!
# equivalent to [(29, 0), (37, 23), (631, 29), (13, 8), (19, 10), (23, 6), (383, 60), (41, 29), (17, 9)]

# a and b will be tuples such that n == a[1] mod a[0] and n == b[1] mod b[0]
def crt(a, b):
    # throw out non-coprime case (won't come up here but whatever)
    if not math.gcd(a[0],b[0]) == 1:
        print('attempted to do crt with non-coprime integers!!!')
        print('a = ' + str(a))
        print('b = ' + str(b))
        return

    # extended euclidean to get x, y such that a[0]x + b[0]y = 1
    # NOTE - stop at remainder = 0, above is what we want
    quot = [0, 0] # no quotient at first
    # when doing this by hand you'd put larger one first, but it works either way
    rem = [a[0], b[0]]
    # bezout coefficients
    s = [1, 0]
    t = [0, 1]

    # printing euclid part 1
    #for i in [0,1]:
    #    print(quot[i], rem[i], s[i], t[i])

    # current position in list
    i = 2

    # run the algorithm
    while 1:
        quot.append(math.floor(rem[i-2] / rem[i-1]))
        rem.append(rem[i-2] - (quot[i] * rem[i-1]))
        s.append(s[i-2] - (quot[i] * s[i-1]))
        t.append(t[i-2] - (quot[i] * t[i-1]))
        #print(quot[i], rem[i], s[i], t[i]) # printing euclid part 2
        if rem[i] == 0: # the remainder is 0
            break
        i += 1

    # s[i-1] and t[i-1] are the x and y we want, up to sign
    x_maybe = [s[i-1], -s[i-1]]
    y_maybe = [t[i-1], -t[i-1]]
    # get correct sign
    for xm in x_maybe:
        for ym in y_maybe:
            if a[0] * xm + b[0] * ym == 1:
                x = xm
                y = ym
                break
        else:
            continue
        break

    # now we can get the remainder modulo lcm(a[0], b[0]) = a[0]*b[0]
    # z = a[1] mod a[0]
    # z = b[1] mod b[0]
    # a[0]x + b[0]y = 1 ( confirmed )
    # compared to other notation: x -> z, a1 -> a[1], n1 -> a[0], a2 -> b[1], n2 = b[0], m1 -> x, m2 -> y
    z = a[1] * y * b[0] + b[1] * x * a[0]
    # z is the smallest positive integer such that z = a[1] mod a[0] and z = b[1] mod b[0]
    return (a[0]*b[0], z)

# to do this for multiple bois, we reduce
ans = reduce(lambda a,b:crt(a,b),buses)
print('(part b) earliest time = ' + str(ans[1] % ans[0]))
print('checking this with the buses...')
for bus in buses:
    print('bus ' + str(bus[0]) + ' arrives at ' + str(-ans[1] % bus[0]) + ' after this time (supposed to arrive: ' + str(bus[0]-bus[1]) + ')')
    # [(29, 0), (37, 23), (631, 29), (13, 47), (19, 48), (23, 52), (383, 60), (41, 70), (17, 77)]