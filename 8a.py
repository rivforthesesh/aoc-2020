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
ias_list = []
for string in input_list: # 'acc +23'
    ia = string.split(' ') # ('acc', '+23')
    ias_list.append([ia[0], int(ia[1]), 0]) # [['acc', 23, 0]]
    # doing lists so it's mutable

# value of the accumulator starts at 0
acc = 0
# step counts the order of execution
step = 0
# pos has the position of the next instruction in the list
pos = 0

while 1: # loops until break
    step += 1 # increase step
    ias = ias_list[pos]
    i = ias[0]
    a = ias[1]
    s = ias[2]
    #print(str(ias) + ' at pos ' + str(pos))
    if s > 0: # instruction has been visited
        print('returned to ' + i + ' ' + str(a) + ' at step ' + str(step) + ', previously visited at step ' + str(s))
        print('acc = ' + str(acc))
        break
    # o/w execute instruction
    if i == 'jmp':
        ias_list[pos][2] = step # put step in the list in the list
        pos += a # jump to instruction
        continue # back to while
    elif i == 'nop':
        ias_list[pos][2] = step # put step in the list in the list
        pos += 1 # next instruction
        continue # back to while
    elif i == 'acc':
        ias_list[pos][2] = step  # put step in the list in the list
        acc += a # add the argument to acc
        pos += 1 # next instruction
        continue # back to while
    else:
        print('incorrect instruction: ' + i + ' at position ' + str(pos))