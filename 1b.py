# find the three entries that sum to 2020 and then multiply those three numbers together

# input
with open('1.txt', 'r') as file:
    input = file.read()

# turn the input into a list
list_str = list(input.split('\n'))

# get a list of ints
list_int = []
for k in list_str:
    list_int.append(int(k))

# find the pair and multiply them
for i in list_int:
    for j in list_int:
        for k in list_int:
            if i + j + k == 2020:
                print(i*j*k)