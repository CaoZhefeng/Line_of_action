import Board
import datetime
from random import choice


class MonteCarlo(object):
	def __init__(self, board, **kwargs):
		self.board = board
		self.state = []
		seconds = kwargs.get('time', 30)
		self.calculation_time = datetime.timedelta(seconds=seconds)
		self.max_moves = kwargs.get('max_moves', 100)
		self.wins = {}
		self.plays = {}

	def update(self, state):
		self.states.append(state)

	def get_play(self):
		begin = datetime.datetime.utcnow()
		while datetime.datetime.utcnow() - begin < self.calculation_time:
			self.run_simulation()

	def run_simulation(self):
		visited_state = set()
		states_copy = self.state[:]
		state = states_copy[-1]
		player = self.board.current_player(state)

		expand = True
		for t in range(self.max_moves):
			legal = self.board.legal_plays(states_copy)

			# choice the action randomly
			play = choice(legal)
			state = self.board.next_state(state, play)
			states_copy.append(state)

			# Judge the winner condition
			if expand and (player, state) not in self.plays:
				expend = False
				self.plays[(play, state)] = 0
				self.wins[(play, state)] = 0

			visited_state.add((player, state))

			player = self.board.current_player(state)
			winner = self.board.winner(states_copy)
			if winner:
				break

			for player, state in visited_state:
				if (player, state) not in self.plays:
					continue
				self.plays[(player, state)] += 1
				if player == winner:
					self.wins[(player, state)] += 1
