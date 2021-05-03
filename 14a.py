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
        # e.g. line = 'mem[25226] = 65531297'

        # find where the close bracket is
        close_bracket = line.find(']')
        mem_loc = int(line[4:close_bracket])
        # mem_loc = 25226

        # find where the = is
        equals = line.find('=')
        mem_val = int(line[(equals+1):])
        # mem_val = 65531297

        # get mem_val as binary
        mem_bin = bin(mem_val)[2:]
        # slice to remove the '0b'
        # mem_bin = '11111001111110110110100001'

        # add on leading zeroes if needed
        if len(mask) > len(mem_bin):
            mem_bin = ('0' * (len(mask) - len(mem_bin))) + mem_bin
        # mem_bin = '000000000011111001111110110110100001'

        # split into characters
        mask_chars = list(mask)
        memb_chars = list(mem_bin)
        # apply mask
        for i in range(0,len(mask)):
            # change memb_char if not X
            if not mask_chars[i] == 'X':
                memb_chars[i] = mask_chars[i]
        # overwrite mem_bin with the concatenation of memb_chars
        mem_bin = ''.join(memb_chars)

        # get int from str
        mem_val = int(mem_bin,2)
        # add to dict
        mem_dict[mem_loc] = mem_val

# mem filled
print('sum of mem values (part a): ' + str(sum(list(mem_dict.values()))))
