# catching the bus
# starting at the time you arrive, which bus can you get first
# (what multiple shows up first)

# input
with open('13.txt', 'r') as file:
    input = file.read()

# turn the input into a list - this has when you arrive and the list of buses
input_list = list(input.split('\n'))
# get your buses
buses_str = input_list[1].split(',')
# turn the ones in service into ints and gets the dt we need
buses = []
for bus_str in buses_str:
    if not bus_str == 'x':
        buses.append(int(bus_str))

# get biggest bus: this is your step
big_bus = max([int(bus_str) for bus_str in buses_str if not bus_str == 'x'])
# assume each bus unique; get dt needed
big_plus = 0
for bus in buses:
    if not bus == big_bus:
        big_plus += 1

# timestamp; hint is that it'll be after this one
t = 100000000000000 - big_plus
# loop indefinitely
while 1:
    print('t = ' + str(t), end='\r',flush=True)
    # reset dt (time difference from t)
    dt = 0
    # check each bus
    for b in range(0,len(buses)):
        bus = buses[b]
        # if we need a bus to arrive at this time
        if not bus == 'x':
            # if that bus does not arrive
            if not (t + dt) % bus == 0:
                # t is not our timestamp
                break
        dt += 1 # increment time diff
    else: # did not break
        print('part b answer: ' + str(t))
    # for loop broke
    # increment time by amount of first bus
    t += big_bus