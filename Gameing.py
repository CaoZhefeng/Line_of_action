from Human import Human
from MCTS_fun import MCTS
from random import choice


class Game(object):
	"""
	game server
	"""

	def __init__(self, board, **kwargs):
		self.board = board
		self.player = [0, 1]  # 0为白棋方/ 1为黑棋方
		self.time = float(kwargs.get('time', 5))  # 默认每步计算时长为5s
		self.max_actions = int(kwargs.get('max_actions', 1000))  # 默认每次模拟对局最多进行的步数为1000

	def start(self):
		p1, p2 = self.init_player()  # 随机给出下子顺序, p1为AI，p2为Human
		self.board.init_board([1, 0])  # 黑方先下

		ai = MCTS(self.board)
		human = Human(self.board)
		players = {}
		players[p1] = ai
		players[p2] = human
		turn = [1, 0]  # 黑棋先走

		while (1):
			p = turn.pop(0)  # 回合制,p为当前的棋的颜色
			turn.append(p)
			player_in_turn = players[p]  # 此回合的下子方，数据类型为类

			# 棋手同步棋盘
			if p == p1:
				player_in_turn.root.state = self.board
			else:
				player_in_turn.state = self.board

			# 得到当前可下的步骤
			position, move = player_in_turn.get_action()
			self.board = self.board.update(position, move)  # 更新棋盘
			self.graphic(self.board, p1, p2)

			end_or_not, winner = self.board.has_a_winner()
			if end_or_not:
				if winner != -1:
					print("Game end. Winner is", players[winner])
				else:
					print("Tie")
				break

	def init_player(self):  # 玩家和电脑随机确定下棋方
		plist = list(range(len(self.player)))
		index1 = choice(plist)
		plist.remove(index1)
		index2 = choice(plist)

		return self.player[index1], self.player[index2]

	def graphic(self, board, AI_player, Human_player):
		"""
		在终端绘制棋盘，显示棋局的状态
		"""
		width = board.width
		height = board.height
		Relationship = {0: "white with O", 1: "Black with X"}

		print("Human Player", Relationship[Human_player])
		print("AI    Player", Relationship[AI_player])
		print()
		for x in range(width):
			print("{0:8}".format(x), end='')
		print('\r\n')
		for i in range(height - 1, -1, -1):
			print("{0:4d}".format(i), end='')
			for j in range(width):
				loc = i * width + j
				if board.states[loc] == 1:  # 黑棋
					print('X'.center(8), end='')
				elif board.states[loc] == 0:  # 白棋
					print('O'.center(8), end='')
				else:
					print('_'.center(8), end='')
			print('\r\n\r\n')
