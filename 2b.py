# Each line gives the password policy and then the password.
# Each policy actually describes two positions in the password, where 1 means the first character,
#   2 means the second character, and so on.
# (Be careful; Toboggan Corporate Policies have no concept of "index zero"!)
# Exactly one of these positions must contain the given letter.
# Other occurrences of the letter are irrelevant for the purposes of policy enforcement.
# For example, 1-3 a means that the password must contain a at position 1 (0) xor at position 3 (0).

# input
with open('2.txt', 'r') as file:
    input = file.read()

# turn the input into a list; each entry is '1-3 a: abcde'
input_list = list(input.split('\n'))

# break it up into tuples
password_rules = []
for str in input_list:
    tmp_tuple = str.split(' ') # ('1-3', 'a:', 'abcde')
    range = tmp_tuple[0].split('-') # ('1', '3')
    letter = tmp_tuple[1][:-1] # 'a' (removes last character)
    password_rules.append((int(range[0]), int(range[1]), letter, tmp_tuple[2])) # (1, 3, 'a', 'abcde')

# check each string against the rules
good_pw = [] # these pass the check
bad_pw = [] # these fail the check
for tuple in password_rules:
    i = tuple[0]
    j = tuple[1]
    letter = tuple[2]
    password = tuple[3]
    letij = 0 # how many times the letter appears in position i or j
    if password[i-1] == letter:
        letij += 1
    if password[j-1] == letter:
        letij += 1
    if letij == 1: # if the letter appears in i xor j ((i and ¬j) or (¬i and j))
        good_pw.append(password) # it is a good password
    else: # the letter is in neither or both positions
        bad_pw.append(password) # it is a bad password

# the passwords are in good_pw and bad_pw lists
print(len(good_pw))