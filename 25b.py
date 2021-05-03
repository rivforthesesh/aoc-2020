import os

print('why did you download this')
for num in range(1,26):
    for let in ['a','b']:
        print('running ' + str(num) + let + '...')
        os.system('python ' + str(num) + let + '.py')