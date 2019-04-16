# specific game information
import numpy as np

class Board(object):

	def __init__(self, width=8, height=8):
		self.width = width
		self.height = height
		self.states = {}  # 记录当前棋盘的状态，键是位置，值是棋子，这里用玩家来表示棋子类型
		self.acquirability = set()

	def init_board(self):
		## 初始化棋盘
		for m in list(range(self.width * self.height)):
			h = m // self.width
			w = m % self.width
			if (h == 0 and w != 0 and w != self.width - 1) or (h == self.height - 1 and w != 0 and w != self.width - 1):
				self.states[m] = 0  # 0表示当前位置为白棋,O
			elif (w == 0 and h != 0 and h != self.width - 1) or (
					w == self.height - 1 and h != 0 and h != self.width - 1):
				self.states[m] = 1  # 1表示当前位置为黑棋,X
			else:
				self.states[m] = -1  # -1表示当前位置为空

	# 返回所下棋子的位置
	def move_to_location(self, move):
		h = move // self.width
		w = move % self.width
		return [h, w]

	def location_to_move(self, location):
		if (len(location) != 2):
			return -1
		h = location[0]
		w = location[1]
		move = h * self.width + w
		if (move not in range(self.width * self.height)):
			return -1
		return move

	def get_available(self, player):
		if player==1: # 黑棋方正在下棋
			enemy=0 # 对方为黑棋
		else:
			enemy=1 # 对方为黑棋

		acquirability = set()
		for m in list(range(self.width * self.height)):
			h = m // self.width
			w = m % self.width

			if self.states[m] == player:
				# 判断横向走法
				t = 0
				for n in range(self.width):  # 计算此line上有几颗棋子
					if self.states[h * self.width + n] != -1:
						t = t + 1
				if w - t > 0 and self.states[m - t] != player:  # 判断所下子在棋盘内且目标位置没有己方棋子
					if enemy not in self.states[m-t:1:m]:  # 判断路径上没有敌棋
						acquirability.add((m, m - t))
				if w + t < self.width and self.states[m + t] != player:
					if enemy not in self.states[m:1:m+t]:
						acquirability.add((m, m + t))

				# 判断纵向走法
				t = 0
				for n in range(self.height):
					if self.states[n * self.width + w] != -1:
						t = t + 1
				if h - t > 0 and self.states[m - t * self.width] != player:
					if enemy not in self.states[m - t * self.width:self.width:m]:
						acquirability.add((m, m - t * self.width))
				if h + t < self.height and self.states[m + t * self.width] != player:
					if enemy not in self.states[m:self.width:m + t * self.width]:
						acquirability.add((m, m + t * self.width))

				# 判断正斜向走法
				t = 0
				if w > h:
					w_least = w - h
					h_least = 0
				else:
					w_least = 0
					h_least = h - w

				for n in range(min(self.width - w_least, self.height - h_least)):
					if self.states[(n + h_least) * self.width + w_least + n] != -1:
						t = t + 1
				if m - t * (self.width + 1) > 0 and self.states[m - t * (self.width + 1)] != player:
					if enemy not in self.states[m - t * (self.width + 1):self.width+1:m]:
						acquirability.add((m, m - t * (self.width + 1)))
				if m + t * (self.width + 1) < self.height * self.width and self.states[
					m + t * (self.width + 1)] != player:
					if enemy not in self.states[m:self.width + 1:m + t * (self.width + 1)]:
						acquirability.add((m, m + t * (self.width + 1)))

				# 判断副斜向走法
				t = 0
				if w + h < self.width:
					w_least = w + h
					h_least = 0
				else:
					w_least = self.width - 1
					h_least = h + w + 1 - self.width

				for n in range(min(self.height - h_least, w_least)):
					if self.states[(n + h_least) * self.width + w_least - n] != -1:
						t = t + 1
				if m - t * (self.width - 1) > 0 and self.states[m - t * (self.width - 1)] != player:
					if enemy not in self.states[m - t * (self.width - 1):self.width - 1:m]:
						acquirability.add((m, m - t * (self.width - 1)))
				if m + t * (self.width - 1) < self.height * self.width and self.states[
					m + t * (self.width - 1)] != player:
					if enemy not in self.states[m:self.width - 1:m + t * (self.width - 1)]:
						acquirability.add((m, m + t * (self.width - 1)))

		return acquirability

	def update(self, player, position, move):  # player在move处落子，更新棋盘
		self.states[move] = player
		self.states[position] = -1  # 原位置为空

	def has_a_winner(self):
		"""
		检查是否有玩家获胜
		"""
		width = self.width
		height = self.height
		states = np.array(self.states)
		black = 1
		white = 0
		all_black_chess = np.where(states == black)
		all_white_chess = np.where(states == white)

		# 判断单个棋子的获胜情况
		if len(all_black_chess[0] == 1):
			return True, black
		if len(all_white_chess == 1):
			return True, white

		# 判断联通情况
		# 黑棋
		visited = [0 for i in range(len(self.states))]
		connection = {all_black_chess[0][0]}
		flag = 1  # flag为0表示存在多个连通区域, 1为只有一个连通区域
		while len(connection):
			m = connection.pop()
			visited[m] = 1
			h_m = m // width
			w_m = m % width
			for n in all_black_chess[0]:
				h_n = n // width
				w_n = n % width
				if abs(h_m - h_n) <= 1 and abs(w_m - w_n) <= 1 and visited[n] == 0:
					connection.add(n)
			connection.remove(m)
		for m in all_black_chess[0]:
			if visited[m] == 0:
				flag = 0
				break
		if flag == 1:
			return True, black

		# 白棋
		visited = [0 for i in range(len(self.states))]
		connection = {all_white_chess[0][0]}
		flag = 1  # flag为0表示存在多个连通区域, 1为只有一个连通区域
		while len(connection):
			m = connection.pop()
			visited[m] = 1
			h_m = m // width
			w_m = m % width
			for n in all_white_chess[0]:
				h_n = n // width
				w_n = n % width
				if abs(h_m - h_n) <= 1 and abs(w_m - w_n) <= 1 and visited[n] == 0:
					connection.add(n)
			connection.remove(m)
		for m in all_white_chess[0]:
			if visited[m] == 0:
				flag = 0
				break
		if flag == 1:
			return True, white

		# 若均没有人获胜则返回-1
		return False, -1