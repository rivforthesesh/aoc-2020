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

# make it a function returning the winner
def play_game(p1,p2,depth=0):
    # get list for previous configurations
    prev = []
    # while both players still have cards
    while min(len(p1), len(p2)) > 0:
        # check if p1 should win
        # card is in prev configs but not latest one
        if (p1, p2) in prev:
            print(str(depth) + ':' + '  '*depth + 'p1 won by previous config',end='\r',flush=True)
            # end game with p1 winning
            return 1

        # save card config
        prev.append((p1.copy(),p2.copy()))

        # grab first two cards
        c1 = p1.pop(0)
        c2 = p2.pop(0)

        # show cards with depth
        print(str(depth) + ':' + '  '*depth + 'c1 =',c1,'c2 =',c2,end='\r',flush=True)

        # check if players have at least as many cards remaining as the number they just drew
        if len(p1) >= c1 and len(p2) >= c2:

            # winner determined by a new game of recursive combat
            sub_winner = play_game(p1[:c1],p2[:c2],depth+1)
            if sub_winner == 1:
                p1.append(c1)
                p1.append(c2)
            elif sub_winner == 2:
                p2.append(c2)
                p2.append(c1)
        else:
            # otherwise, player with higher card wins
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
    if not p1:
        print(str(depth) + ':' + '  '*depth + 'p2 won                          ',end='\r',flush=True)
        return 2
    elif not p2:
        print(str(depth) + ':' + '  '*depth + 'p1 won                          ',end='\r',flush=True)
        return 1

winner = play_game(p1,p2)

score = 0
if winner == 2:
    print('p2 won!!')
    for i in range(0,len(p2)):
        score += p2[i]*(len(p2)-i)
elif winner == 1:
    print('p1 won!!')
    for i in range(0, len(p1)):
        score += p1[i] * (len(p1) - i)

print('score:',score)