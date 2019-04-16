import time
import copy
import math


class MCTS(object):
	"""
	AI player, use Monte Carlo Tree Search with UCB
	"""

	def __init__(self, board, player_turn, time=5, max_actions=1000):

		self.board = board
		self.player_turn = player_turn  # 出手顺序——两个数
		self.calculation_time = float(time)  # 最大运算时间
		self.max_actions = max_actions  # 每次模拟对局最多进行的步数

		self.player = player_turn[0]  # 轮到电脑出手，所以出手顺序中第一个总是电脑
		self.confident = 1.96  # UCB中的常数
		self.plays = {}  # 记录着法参与模拟的次数，键形如(player, position, move)，即（玩家，所选棋子，落子）
		self.wins = {}  # 记录着法获胜的次数
		self.max_depth = 1

	def get_action(self):  # return position and move
		"""
			修改可选的下一步根据现有己方棋子来枚举
		"""

		# 每次计算下一步时都要清空plays和wins表，因为经过AI和玩家的2步棋之后，整个棋盘的局面发生了变化，原来的记录已经不适用了——原先普通的一步现在可能是致胜的一步，如果不清空，会影响现在的结果，导致这一步可能没那么“致胜”了
		self.plays = {}
		self.wins = {}
		simulations = 0  # 模拟次数
		begin = time.time()
		while time.time() - begin < self.calculation_time:
			board_copy = copy.deepcopy(self.board)  # 模拟会修改board的参数，所以必须进行深拷贝，与原board进行隔离
			player_turn_copy = copy.deepcopy(self.player_turn)  # 每次模拟都必须按照固定的顺序进行，所以进行深拷贝防止顺序被修改
			self.run_simulation(board_copy, player_turn_copy)  # 进行MCTS
			simulations += 1

		print("total simulations=", simulations)

		position, move = self.select_one_move()  # 选择最佳着法
		location = self.board.move_to_location(move)
		old_loc = self.board.move_to_location(position)
		print('Maximum depth searched:', self.max_depth)

		print("AI move from %d,%d to %d,%d\n" % (old_loc[0], old_loc[1], location[0], location[1]))

		return position, move

	def run_simulation(self, board, player_turn):
		"""
		MCTS main process
		"""

		plays = self.plays
		wins = self.wins

		player = self.get_player(player_turn)  # 获取当前出手的玩家

		# 枚举所有可能下法
		board.acquirability = board.get_available(player)
		acquirability = board.acquirability

		visited_states = set()  # 记录当前路径上的全部着法
		winner = -1
		expand = True

		# Simulation
		for t in range(1, self.max_actions + 1):
			# Selection
			# 如果所有着法都有统计信息，则获取UCB最大的着法
			if all(plays.get((player, position, move)) for (position, move) in acquirability):
				log_total = math.log(
					sum(plays[(player, position, move)] for (position, move) in acquirability))
				value, position, move = max(
					((wins[(player, position, move)] / plays[(player, position, move)]) +
					 math.sqrt(self.confident * log_total / plays[(player, position, move)]), position, move)
					for (position, move) in acquirability)
			else:
				# 否则随机选择一个着法??????????
				position, move = acquirability.pop()

			# 更新棋盘
			board.update(player, position, move)

			# Expand
			# 每次模拟最多扩展一次，每次扩展只增加一个着法
			if expand and (player, position, move) not in plays:
				expand = False
				plays[(player, position, move)] = 0
				wins[(player, position, move)] = 0
				if t > self.max_depth:
					self.max_depth = t

			visited_states.add((player, position, move))

			win, winner = self.board.has_a_winner()
			if win:  # 游戏结束，有玩家获胜
				break

			player = self.get_player(player_turn)
			# 更新对方所有下法
			board.acquirability = board.get_available(player)
			acquirability = board.acquirability

		# Back-propagation
		for player, position, move in visited_states:
			if (player, position, move) not in plays:
				continue
			plays[(player, position, move)] += 1  # 当前路径上所有着法的模拟次数加1
			if player == winner:
				wins[(player, position, move)] += 1  # 获胜玩家的所有着法的胜利次数加1

	def get_player(self, players):
		p = players.pop(0)
		players.append(p)
		return p

	def select_one_move(self):
		percent_wins, position, move = max(  # 只比较第一个值的大小
			(self.wins.get((self.player, position, move), 0) /
			 self.plays.get((self.player, position, move), 1),
			 position, move)
			for (position, move) in self.board.acquirability)  # 选择胜率最高的着法

		return position, move

	def __str__(self):
		return "AI"
