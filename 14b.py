# bit masks

# input
with open('14.txt', 'r') as file:
    input = file.read()

# turn the input into a list - this has either a mask or a mem
input_list = list(input.split('\n'))
# have the mem as a dict
mem_dict = {}

for line in input_list:
    if line[:4] == 'mask': # if this is a mask line
        mask = line[7:] # store the mask - str after 'mask = '
    elif line[:3] == 'mem': # if this is a mem line
        # same as before:
        close_bracket = line.find(']')
        mem_loc = int(line[4:close_bracket])
        equals = line.find('=')
        mem_val = int(line[(equals+1):])
        mem_bin = bin(mem_loc)[2:]
        if len(mask) > len(mem_bin):
            mem_bin = ('0' * (len(mask) - len(mem_bin))) + mem_bin
        mask_chars = list(mask)
        memb_chars = list(mem_bin)

        # apply mask
        for i in range(0,len(mask)):
            # floating if X (either 0 or 1)
            if mask_chars[i] == 'X':
                memb_chars[i] = 'X'
            # set bit as 1 if 1
            elif mask_chars[i] == '1':
                memb_chars[i] = '1'

        # get list of all possible mem_locs
        mem_locs = ['']
        for i in range(0,len(mask)):
            # if this is a floating bit
            if memb_chars[i] == 'X':
                # add 0 to every string
                mems0 = []
                for mem_bin in mem_locs:
                    mems0.append(mem_bin + '0')
                # add 1 to every string
                mems1 = []
                for mem_bin in mem_locs:
                    mems1.append(mem_bin + '1')
                # make both of these lists together the new list
                mem_locs = mems0 + mems1
            else: # this is '0' or '1'
                # append this to all lists in the string
                for j in range(0,len(mem_locs)):
                    mem_locs[j] = mem_locs[j] + memb_chars[i]

        for mem_bin in mem_locs:
            # get int from str
            mem_loc = int(mem_bin,2)
            # add to dict
            mem_dict[mem_loc] = mem_val

# mem filled
print('sum of mem values (part b): ' + str(sum(list(mem_dict.values()))))

# 11538359040 too low