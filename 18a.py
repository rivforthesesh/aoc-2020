# bidmas but we only care about the b

# input
with open('18.txt', 'r') as file:
    input = file.read()

# turn the input into a list
input_list = list(input.split('\n'))

def go_brrr(string):
    # count number of open brackets
    num_brackets = len([char for char in string if char == '('])
    if num_brackets == 0:
        # no brackets => just evaluate left to right
        num_plus = len([char for char in string if char == '+'])
        num_times = len([char for char in string if char == '*'])
        if num_times == 0:
            # sums only, or no ops left
            return eval(string)
        elif num_plus == 0:
            # products only
            return eval(string)
        else: # mix of sums and products
            # go one op at a time
            ns = string.split(' ',3)
            # string = 3 * 4 + 8 + 5
            # ns = ['3', '*', '4', ' + 8 + 5']
            # apply go_brrr to '12 + 8 + 5'
            return go_brrr(str(eval(ns[0]+ns[1]+ns[2])) + ' ' + ns[3])
    else: # we have brackets
        # get the expression between the first close bracket
        # and the last open bracket preceding it
        # string = '((2 * 9 + 4 + 5) * 5) + 2'
        tmp1 = string.split(')',1)
        # tmp1 = ['((2 * 9 + 4 + 5', ' * 5) + 2']
        tmp2 = tmp1[0].rsplit('(',1)
        # tmp2 = ['(', '2 * 9 + 4 + 5']
        before_expr = ''.join(tmp2[:-1])
        # before_expr = '('
        expr = tmp2[-1]
        # expr = '2 * 9 + 4 + 5'
        after_expr = ''.join(tmp1[1:])
        # after_expr = ' * 5) + 2'
        return go_brrr(before_expr + str(go_brrr(expr)) + after_expr)

sum = 0
for line in input_list:
    sum += int(go_brrr(line))
print(sum)