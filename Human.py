from random import choice


class Human(object):
	"""
	human player
	"""

	def __init__(self, board):
		self.state = board

	def get_action(self):
		# old_loc = [int(n, 10) for n in input("choose your chess: ").split(",")]
		# location = [int(n, 10) for n in input("move to: ").split(",")]
		# move = self.state.location_to_move(location)
		# position = self.state.location_to_move(old_loc)
		#
		# if (position, move) not in self.state.acquirability:
		# 	print("invalid move")
		# 	position, move = self.get_action()

		position, move = choice(list(self.state.acquirability))
		return position, move

	def __str__(self):
		return "Human"
