# cards

# input
with open('22.txt', 'r') as file:
    input = file.read()

# turn the input into a list
input_list = list(input.split('\n'))

# set up dict for player cards
cards_dict = {}
player_num = 0

# get current player and their cards
while len(input_list) > 0:
    line = input_list.pop(0)
    # skip if empty
    if line == '':
        continue
    # change player number if player
    if line[:6] == 'Player':
        player_num = int(line.replace('Player ','').replace(':',''))
        cards_dict[player_num] = []
        continue
    # add card if card
    cards_dict[player_num] = cards_dict[player_num] + [int(line)]

# we now have a list of cards for each player
# make it a two-player game bc easier
p1 = cards_dict[1]
p2 = cards_dict[2]

# while both players still have cards
while min(len(p1),len(p2)) > 0:
    # grab first two cards
    c1 = p1.pop(0)
    c2 = p2.pop(0)
    # player with highest card places their card at the bottom of their pile
    # and the other player's card below that
    if c1 > c2:
        p1.append(c1)
        p1.append(c2)
    elif c1 < c2:
        p2.append(c2)
        p2.append(c1)
    else:
        print('oh shit the cards are the same')
        break

score = 0
if not p1:
    print('p2 won!')
    for i in range(0,len(p2)):
        score += p2[i]*(len(p2)-i)
elif not p2:
    print('p1 won!')
    for i in range(0, len(p1)):
        score += p1[i] * (len(p1) - i)

print('score:',score)