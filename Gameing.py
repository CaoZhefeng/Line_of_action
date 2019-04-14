from Human import Human
from MCTS_fun import MCTS
from random import choice, shuffle


class Game(object):
	"""
	game server
	"""

	def __init__(self, board, **kwargs):
		self.board = board
		self.player = [1, 2]  # player1 and player2
		self.n_in_row = int(kwargs.get('n_in_row', 5))  # 默认连成5个获胜
		self.time = float(kwargs.get('time', 5))  # 默认每步计算时长为5s
		self.max_actions = int(kwargs.get('max_actions', 1000))  # 默认每次模拟对局最多进行的步数为1000

	def start(self):
		p1, p2 = self.init_player()  # 随机给出下子顺序
		self.board.init_board()

		ai = MCTS(self.board, [p1, p2], self.n_in_row, self.time, self.max_actions)
		human = Human(self.board, p2)
		players = {}
		players[p1] = ai
		players[p2] = human
		turn = [p1, p2]
		shuffle(turn)  # 玩家和电脑的出手顺序随机
		while (1):
			p = turn.pop(0)  # 回合制
			turn.append(p)
			player_in_turn = players[p]  # 此回合的下子方
			move = player_in_turn.get_action()
			self.board.update(p, move)
			self.graphic(self.board, human, ai)
			end, winner = self.game_end(ai)
			if end:
				if winner != -1:
					print("Game end. Winner is", players[winner])
				break

	def init_player(self):
		plist = list(range(len(self.player)))
		index1 = choice(plist)
		plist.remove(index1)
		index2 = choice(plist)

		return self.player[index1], self.player[index2]

	def game_end(self, ai):
		"""
		检查游戏是否结束
		"""
		win, winner = ai.has_a_winner(self.board)
		if win:
			return True, winner
		elif not len(self.board.availables):  # 平局
			print("Game end. Tie")
			return True, -1
		return False, -1

	def graphic(self, board, human, ai):
		"""
		在终端绘制棋盘，显示棋局的状态
		"""
		width = board.width
		height = board.height

		print("Human Player", human.player, "with X".rjust(3))
		print("AI    Player", ai.player, "with O".rjust(3))
		print()
		for x in range(width):
			print("{0:8}".format(x), end='')
		print('\r\n')
		for i in range(height - 1, -1, -1):
			print("{0:4d}".format(i), end='')
			for j in range(width):
				loc = i * width + j
				if board.states[loc] == human.player:
					print('X'.center(8), end='')
				elif board.states[loc] == ai.player:
					print('O'.center(8), end='')
				else:
					print('_'.center(8), end='')
			print('\r\n\r\n')
