# from Gameing import Game
# from Board import Board
#
# b=Board()
# game1=Game(b)
# game1.start()
import random


def get_player(players):
	p = players.pop(0)
	players.append(p)
	return p

play=[0,1]
p=get_player(play)

print(p)
print(play)