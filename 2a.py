# Each line gives the password policy and then the password.
# The password policy indicates the lowest and highest number of times a given letter
#   must appear for the password to be valid.
# For example, 1-3 a means that the password must contain a at least 1 time and at most 3 times.


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
    min = tuple[0]
    max = tuple[1]
    letter = tuple[2]
    pw_temp = password = tuple[3]
    is_good = False
    let_count = 0
    while len(pw_temp) > 0: # while the string is nonempty
        pw_let = pw_temp[0] # first character
        if pw_let == letter: # if the pw_let is the letter you're checking for
            let_count += 1
        pw_temp = pw_temp[1:] # removes first character from string
    if let_count >= min and let_count <= max: # it satisfies the conditions
        good_pw.append(password) # add to good password list
    else: # it does not satisfy the conditions
        bad_pw.append(password) # add to bad password list

# the passwords are in good_pw and bad_pw lists
print(len(good_pw))