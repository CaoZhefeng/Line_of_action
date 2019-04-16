class Human(object):
	"""
	human player
	"""

	def __init__(self, board, player):
		self.board = board
		self.player = player

	def get_action(self):
		old_loc = [int(n, 10) for n in input("choose your chess: ").split(",")]
		location = [int(n, 10) for n in input("move to: ").split(",")]
		move = self.board.location_to_move(location)
		position = self.board.location_to_move(old_loc)

		if (position, move) not in self.board.acquirability:
			print("invalid move")
			position, move = self.get_action()
		return position, move

	def __str__(self):
		return "Human"
