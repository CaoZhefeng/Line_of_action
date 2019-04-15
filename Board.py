# specific game


class Board(object):

	def __init__(self, width=8, height=8):
		self.width = width
		self.height = height
		self.states = {}  # 记录当前棋盘的状态，键是位置，值是棋子，这里用玩家来表示棋子类型
		self.availables = set()

	def init_board(self):
		## 初始化棋盘
		for m in list(range(self.width * self.height)):
			if m // self.width == 0 and m % self.width != 0 and m % self.width != self.width - 1:
				self.states[m] = 0  # 0表示当前位置为白棋,O
			elif m // self.width == self.width - 1 and m % self.width != 0 and m % self.width != self.width - 1:
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
		availables = set()
		for m in list(range(self.width * self.height)):
			h = m // self.width
			w = m % self.width

			if self.states[m] == player:
				# 判断横向走法
				t = 0
				for n in range(self.width):  # 计算此line上有几颗棋子
					if self.states[h * self.width + n] != -1:
						t = t + 1
				if w - t > 0 and self.states[m - t] != player:
					availables.add((m, m - t))
				if w + t < self.width and self.states[m + t] != player:
					availables.add((m, m + t))

				# 判断纵向走法
				t = 0
				for n in range(self.height):
					if self.states[n * self.width + w] != -1:
						t = t + 1
				if h - t > 0 and self.states[m - t * self.width] != player:
					availables.add((m, m - t * self.width))
				if h + t < self.height and self.states[m + t * self.width] != player:
					availables.add((m, m + t * self.width))

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
					availables.add((m, m - t * (self.width + 1)))
				if m + t * (self.width + 1) < self.height * self.width and self.states[
					m + t * (self.width + 1)] != player:
					availables.add((m, m + t * (self.width + 1)))

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
					availables.add((m, m - t * (self.width - 1)))
				if m + t * (self.width - 1) < self.height * self.width and self.states[
					m + t * (self.width - 1)] != player:
					availables.add((m, m + t * (self.width - 1)))

		return availables

	def update(self, player, position, move):  # player在move处落子，更新棋盘
		self.states[move] = player
		self.states[position] = -1  # 原位置为空
# self.availables = self.get_available(player)  # 更新可下的步 ？？
