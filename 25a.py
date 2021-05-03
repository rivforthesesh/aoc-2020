# cryptography

# input
with open('25.txt', 'r') as file:
    input = file.read()
input_list = input.split('\n')

# get the public keys
c_pk = int(input_list[0])
d_pk = int(input_list[1])

# set up
c = 1
d = 1
# loop size 7725934 for d
loop = 0
s = 7

# keep multiplying until we get loop sizes
while 1:
    print('loop',loop,'c',c,'d',d,end='\r',flush=True)
    if not c == c_pk:
        c = (c * s) % 20201227
    else:
        loop_found = 'c'
        break
    if not d == d_pk:
        d = (d * s) % 20201227
    else:
        loop_found = 'd'
        break
    loop += 1

# e = 7^c_loop^d_loop = 7^d_loop^c_loop (mod 20201227)
# e = c_pk ^ d_loop

print('')
print('loop found =',loop_found)
print('loop size =',loop)

e = 1 # encryption key
i = 0 # number of loops
if loop_found == 'c':
    while i < loop:
        e = (e * d_pk) % 20201227
        i += 1
else:
    while i < loop:
        e = (e * c_pk) % 20201227
        i += 1

print('encryption key (part a):',e)

# not c_pk * d_pk
# >  2797563, so not repeated c * d. (above)
# < 20054134, so not c_pk^d_loop unless off by one
# ?  5047594, so not c_pk^c_loop
# ?  9177973 (if i did off by one error for c_pk^d_loop)
# 17673381