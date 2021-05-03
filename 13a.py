# catching the bus
# starting at the time you arrive, which bus can you get first
# (what multiple shows up first)

# input
with open('13.txt', 'r') as file:
    input = file.read()

# turn the input into a list - this has when you arrive and the list of buses
input_list = list(input.split('\n'))
arrival_time = int(input_list[0])
# get your buses
buses_str = input_list[1].split(',')
# limit to the ones in service (not x)
buses = [int(bus_str) for bus_str in buses_str if not bus_str == 'x']

# now look at buses
time = arrival_time
# loop indefinitely
while 1:
    # check each bus
    for bus in buses:
        # has the bus arrived?
        if time % bus == 0:
            print('got bus ' + str(bus) + ' at time ' + str(time))
            print('part a answer (bus num * time waited): ' + str(bus*(time-arrival_time)))
            break
    else: # did not break
        # increment time
        time += 1
        continue
    # for loop broke => we get to here
    break