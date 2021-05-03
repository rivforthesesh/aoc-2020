import copy

# acc increases or decreases a single global value called the accumulator by the value given in the argument
# jmp jumps to a new instruction relative to itself.
#   The next instruction to execute is found using the argument as an offset from the jmp instruction;
#   for example,    jmp +2 would skip the next instruction,
#                   jmp +1 would continue to the instruction immediately below it,
#                   jmp -20 would cause the instruction 20 lines above to be executed next
# nop stands for No OPeration - it does nothing. The instruction immediately below it is executed next.

# input
with open('8.txt', 'r') as file:
    input = file.read()

# turn the input into a list, one element is one instruction
input_list = list(input.split('\n'))
# split this into the instruction and the argument, leaving a space for step
ias_list1 = []
for string in input_list: # 'acc +23'
    ia = string.split(' ') # ('acc', '+23')
    ias_list1.append([ia[0], int(ia[1]), 0]) # [['acc', 23, 0]]
    # doing lists so it's mutable

# has the list of instructions that are in the infinite loop
iasp_in_loop = []
# program terminated?
prog_term = False

# first_run is an extra bool for whether this is the first time the function has run
# allows me to use the same function for initial run and 'fixed' run
def do_instructions(list): # executes the list of instructions given in list
    global acc
    global step
    global pos
    global prev_pos
    global iasp_in_loop
    global prog_term
    # value of the accumulator starts at 0
    acc = 0
    # step counts the order of execution
    step = 0
    # pos has the position of the next instruction in the list
    pos = 0
    # prev_pos has the previous position
    prev_pos = 0
    if iasp_in_loop == []: # if the infinite loop isn't recorded
        first_run = True
        print('\ndoing first run...')
    else:
        first_run = False

    while pos < len(list): # goes through until termination
        step += 1  # increase step
        ias = list[pos]
        i = ias[0]
        a = ias[1]
        s = ias[2]
        if first_run:
            iasp_in_loop.append(ias + [pos])
        # print(str(ias) + ' at pos ' + str(pos))
        if s > 0:  # instruction has been visited
            print('returned to ' + i + ' ' + str(a) + ' at step ' + str(step) + ', previously visited at step ' + str(s) + '\n')
            # clear step count - if it's the first run, this list will be reused
            for p in range(0,len(list)):
                list[p][2] = 0
            break
        # o/w execute instruction
        if i == 'jmp':
            list[pos][2] = step  # put step in the list in the list
            pos += a  # jump to instruction
            continue  # back to while
        elif i == 'nop':
            list[pos][2] = step  # put step in the list in the list
            pos += 1  # next instruction
            continue  # back to while
        elif i == 'acc':
            list[pos][2] = step  # put step in the list in the list
            acc += a  # add the argument to acc
            pos += 1  # next instruction
            continue  # back to while
        else:
            print('incorrect instruction: ' + i + ' at position ' + str(pos))
    else: # loop terminated
        print('acc = ' + str(acc))
        prog_term = True

# try to run the instructions, so we find the infinite loop
do_instructions(ias_list1)
print('found infinite loop of ' + str(len(iasp_in_loop)) + ' instructions\n')

# run variants of these instructions with one instruction changed
for iasp in iasp_in_loop:
    i = iasp[0]
    p = iasp[3]
    print(str(iasp))
    # make a copy of ias_list1
    ias_list2 = copy.deepcopy(ias_list1) # by boyf
    # alter the given instruction / skip if acc
    if i == 'jmp':
        ias_list2[p][0] = 'nop'
    elif i == 'nop':
        ias_list2[p][0] = 'jmp'
    else: # it is an acc
        continue
    # run this variant
    print('running variant with ' + str(ias_list2[p]) + ' at position ' + str(p) + '...')
    do_instructions(ias_list2)
    if prog_term:
        break