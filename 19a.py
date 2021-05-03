# languages

# grab itertools for cartesian product
import itertools

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

# build up rules from the bottom up
rules_found = len(rules_str.keys())
total_rules = len(rules.keys()) + rules_found

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

print('                                                  ',end='\r',flush=True)

# part a: checking ones matching rule 0
rule0 = rules_str[0]
matches = 0
for word in input_list:
    if word in rule0:
        matches += 1
        print('matches found: ' + str(matches),end='\r',flush=True)

print('total matches found (part a answer):',matches)

