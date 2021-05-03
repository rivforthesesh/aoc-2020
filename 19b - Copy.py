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
min8 = min42 = min([len(e) for e in r8]) # r8 = r42
min31 = min([len(e) for e in r31])
min11 = min([len(e) for e in r11])
if not min42 + min31 == min11:
    print('something is wrong here!')
min0 = min8 + min11

def is_rule0(word):
    if len(word) < min0: # definitely can't work
        return False
    else:
        # more memory but more speed
        t8 = r8
        t11 = r11
        t42 = r42
        t31 = r31

        # split into the r8 and and r11 sections
        for i in range(min8, len(word) - min11 + 1):
            #print('i =',i,end='\r', flush=True)
            w8 = word[:i] # get start of word
            max8 = math.ceil(len(w8) / min8) # get the max number of times rule 8 will be iterated
            w11 = word[i:] # get end of word
            max11 = math.ceil(len(w11) / min11) # get the max number of times rule 11 will be iterated
            #print(w8, w11, ' '*(max_len-len(word)), end = '\r', flush = True)

            # get a list of words satisfying r8 with at most this number of characters, only one iteration
            t8 = [e for e in t8 if len(e) <= i]
            # get a list of words satisfying r11 with at most this number of characters, only one iteration
            t11 = [e for e in t11 if len(e) <= len(w11)]
            # also get all possible prefixes and suffixes
            t42 = [e for e in t42 if len(e) <= len(w11) - min31]
            t31 = [e for e in t31 if len(e) <= len(w11) - min42]

            w8_done = []
            for j in range(0,max8):
                for v in t8 + ['']: # empty string to allow for words r42
                    n8 = []  # n8 new list to append to t8
                    # if this isn't the start of w8, next v
                    if not v == w8[:len(v)]:
                        continue # next v
                    for w in t8: # try adding on words
                        if len(v+w) <= i:
                            if not v+w in t8 + n8:
                                n8.append(v+w)
                            #print(v, w, end = '\r', flush = True)
                            if v + w == w8 and not w8 in w8_done:
                                w8_done.append(w8)
                                #print(w8,'fits rule 8',' '*(max_len-i))
                                for k in range(0, max11):
                                    # n11 new list to append
                                    n11 = []
                                    for x in t42:
                                        # if this isn't the start of w11, next x
                                        if not x == w11[:len(x)]:
                                            continue # next x
                                        for z in t31:
                                            # if this isn't the end of w11, next z
                                            if not z == w11[-len(z):]:
                                                continue # next z
                                            for y in t11 + ['']: # empty string to allow words r42 + r31
                                                if len(x + y + z) <= len(w11):
                                                    if not x + y + z in t11 + n11:
                                                        n11.append(x + y + z)
                                                    #print(w8, '...', x, y, z, end='\r', flush=True)
                                                    if x + y + z == w11:
                                                        #print(w11, 'fits rule 11',' '*(max_len-len(w11)))
                                                        return True
                                    # add it on
                                    t11 = t11 + n11
                    # add it on
                    t8 = t8 + n8
    return False

print('abababbaba' in r11)

#good_bois = []
for word in input_list:
    print(word)
    if is_rule0(word):
        #good_bois.append(word)
        matches += 1

print('\ntotal matches found (part b answer):',matches)
#print(good_bois)