# languages

# grab itertools for cartesian product
import itertools
# grab math for max number of repeats needed
import math

# input
with open('19.txt', 'r') as file:
    input = file.read()

# turn the input into a list
input_list = list(input.split('\n'))

# read in the rules; these are up to the line break
rules = {}
rules_str = {}
while len(input_list[0]) > 0:
    line = input_list.pop(0)
    # line = '72: 65 104 | 90 95'
    tmp1 = line.split(': ')
    # tmp1 = ['72', '65 104 | 90 95']
    rule_num = int(tmp1[0])
    if '"' in list(tmp1[1]):
        # this just has a letter "a" or "b"
        rule_str = [tmp1[1].replace('"','')]
        rules_str[rule_num] = rule_str
        # print('rule ' + str(rule_num) + ' works with ' + str(len(rule_str)) + ' strings')
        # so '95: "b"' becomes 95: 'b'
    else:
        tmp2 = tmp1[1].split(' | ')
        # tmp2 = ['65 104', '90 95']
        tmp3 = []
        for tmp in tmp2:
            tmp3.append([int(num) for num in tmp.split(' ')])
        # tmp3 = [[65, 104], [90, 95]]
        # set rule
        rules[rule_num] = tmp3

# dict now has our rules
input_list.pop(0)
# input_list is now just the strings

# get maximum list length
max_len = max([len(word) for word in input_list])
print('max_len:', max_len)

# get characters
print('letters that show up:',set([char for word in input_list for char in list(word)]))

# build up rules from the bottom up
rules_found = len(rules_str.keys())
total_rules = len(rules.keys()) + rules_found

# i am NOT implementing the general case
# part a has 128 and 16384 possible strings for 8 and 11 respectively
# modify rules for part b
rules[8] = [[42],[42,8]]
rules[11] = [[42,31],[42,11,31]]

# while we haven't found all the rules
while rules_found < total_rules:
    # for each rule number
    for rule_num in rules.keys():
        # if the list of strings for that rule has not been found
        if not rule_num in rules_str.keys():
            # get the rule for this num (list of lists)
            rule = rules[rule_num]
            # check if every rule it references has been found
            if not [num for rule_op in rule for num in rule_op if not num in rules_str.keys()]:
                # not infinite loop
                # we can directly evaluate this
                tmp = []
                # rule = [[65, 104], [90, 95]]
                for rule_op in rule:
                    # rule_op = [65, 104] => follows rule 65 followed by rule 104
                    # say 65 is ['a', 'b'] and 104 is ['ab', 'ba']
                    tmp1 = list(itertools.product(*[rules_str[rrule_num] for rrule_num in rule_op]))
                    # [('a','ab'), ('b','ba'), ('a','ba'), ('b','ba')]
                    tmp2 = []
                    for tuple in tmp1:
                        string = ''
                        for sub_string in tuple:
                            string = string + sub_string
                        tmp2.append(string)
                    # ['aab', 'aba', 'bab', 'bba']
                    tmp.append(tmp2)
                # say 90 is 'a' and 95 is 'b'
                # tmp = [['aab', 'aba', 'bab', 'bba'], ['a', 'b']]
                # flatten list
                rule_str = [str for str_list in tmp for str in str_list]
                # add string list to dict
                rules_str[rule_num] = rule_str
                # one more rule found
                rules_found += 1
                # print('rule ' + str(rule_num) + ' works with ' + str(len(rule_str)) + ' strings')
                print('determined strings for ' + str(rules_found) + ' of ' + str(total_rules) + ' rules',end='\r',flush=True)
            elif rule_num == 8 and 42 in rules_str.keys(): # can do 8
                # special case for 8
                # 8 can be rule 42, or rule 42 followed by rule 8
                # => 8 can be 42, or 42,42, or 42,42,42
                # => 8 is any number of repetitions of strings satisfying 42

                r8 = r42 = rules_str[42]
                # want to repeat this

                rules_str[rule_num] = r8
                rules_found += 1
                print('determined strings for ' + str(rules_found) + ' of ' + str(total_rules) + ' rules', end='\r',flush=True)

            elif rule_num == 11 and 42 in rules_str.keys() and 31 in rules_str.keys():
                # special case for 11
                # 11 can be rule 42,31 or 42,11,31
                # => 11 can be 42,31, or 42,42,31,31, or 42,42,42,31,31,31
                # => 11 is any number of 42 followed by the same number of 31

                r31 = rules_str[31]
                r42 = rules_str[42]
                r11 = [i + j for i in r42 for j in r31]
                # can put anything in rules_str[42] to the left if you add something in rules_str[31] to the right

                rules_str[rule_num] = r11
                rules_found += 1
                print('determined strings for ' + str(rules_found) + ' of ' + str(total_rules) + ' rules', end='\r', flush=True)

print('                                                  ',end='\r',flush=True)

# part b: checking ones matching rule 0
# rule 0 is 8 11
rule0 = rules_str[0]
matches = 0

min42 = min([len(e) for e in r42])
max42 = max([len(e) for e in r42])
def is_rule42(word, iters):
    if min42 == max42:
        if not len(word) % min42 == 0:
            return(False, 0)
    if word in r42:
        return (True, iters)
    else:
        for x in r42:
            if word[:len(x)] == x:
                result = is_rule42(word[len(x):],iters + 1)
                if result[0]:
                    return result
        return (False, 0)

min31 = min([len(e) for e in r31])
max31 = max([len(e) for e in r31])
def is_rule31(word, iters):
    if min31 == max31:
        if not len(word) % min31 == 0:
            return(False, 0)
    if word in r31:
        return (True, iters)
    else:
        for x in r31:
            if word[:len(x)] == x:
                result = is_rule31(word[len(x):],iters + 1)
                if result[0]:
                    return result
        return (False,0)

def is_rule0(word):
    w = word
    if len(word) < ((2 * min42) + min31): # definitely can't work
        return False
    else:
        c42 = math.ceil((len(word) - min31) / min42) # get the max number of times rule 42 will be iterated
        #c31 = math.ceil((len(word) - 2*min42) / min31)  # get the max number of times rule 31 will be iterated
        # j is the number of words in r42 we have

        for i in range(2 * min42, len(word) - min31 + 1):
            x = word[:i]
            y = word[i:]
            u = is_rule42(x,1)
            v = is_rule31(y,1)
            if u[0] and v[0] and u[1] > 1 and v[1] > 0 and u[1] > v[1]:
                return True
    return False

for word in input_list:
    if is_rule0(word):
        print(word)
        matches += 1

print('\ntotal matches found (part b answer):',matches)

# 407