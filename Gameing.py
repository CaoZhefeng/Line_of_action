from Human import Human
from MCTS_fun import MCTS, MCTNode
from Board import Board
from random import choice
import time


class Game(object):
	"""
	game server
	"""

	def __init__(self, **kwargs):
		self.board = Board([1, 0])  # 黑方先下
		self.board.init_board()  # 初始化棋盘
		self.player = [0, 1]  # 0为白棋方/ 1为黑棋方

	# self.time = float(kwargs.get('time', 5))  # 默认每步计算时长为5s
	# self.max_actions = int(kwargs.get('max_actions', 1000))  # 默认每次模拟对局最多进行的步数为1000

	def start(self):
		p1, p2 = self.init_player()  # 随机给出下子顺序, p1为AI，p2为Human
		Relationship = {p1: "AI", p2: "Human"}

		turn = [1, 0]  # 黑棋先走
		self.graphic(self.board, p1, p2)

		while True:
			p = turn.pop(0)  # 回合制,p为当前的棋的颜色
			turn.append(p)

			# 棋手同步棋盘, 此回合的下子方，数据类型为类
			start_time = time.time()
			if p == p1:
				root = MCTNode(self.board)
				player_in_turn = MCTS(root)
				# 得到当前可下的步骤
				child_node = player_in_turn.get_action()
				self.board = child_node.state

			else:
				player_in_turn = Human(self.board)
				# # 打印可行步
				# self.print_avail()
				# 得到当前可下的步骤
				position, move = player_in_turn.get_action()
				self.board = self.board.update(position, move)  # 更新棋盘

			end_time = time.time()
			print("The cost time of this step:", end_time - start_time, "s")

			self.graphic(self.board, p1, p2)

			end_or_not, winner = self.board.has_a_winner()
			if end_or_not:
				if winner != -1:
					print("Game end. Winner is", Relationship[winner])
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
		print("Now the player is", Relationship[board.player])
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

		print("##########################################################\n")

	def print_avail(self):
		print("Available Step")
		s = list(self.board.acquirability)
		for m in range(len(s)):
			position, move = s[m]
			h_p = position // self.board.width
			w_p = position % self.board.width

			h_m = move // self.board.width
			w_m = move % self.board.width
			print(h_p, w_p, "->", h_m, w_m)


if __name__ == "__main__":
	game1 = Game()
	game1.start()
