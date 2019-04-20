import numpy as np
import random


class MCTNode_2(object):

	def __init__(self, board, parent=None):
		self.parent = parent  # 记录父节点
		self.children = []  # 记录孩子节点
		self._visit_num = 0  # 访问次数
		self._wins_num = 0  # 获胜次数
		self.state = board  # 当前节点对应状态
		self.all_child = board.acquirability

	# 选取该次仿真最佳后代节点
	def best_child(self, c_param=1.4):
		children_value = [(c._wins_num / c._visit_num) + c_param * np.sqrt(2 * np.log(self._visit_num) / c._visit_num)
						  for c in self.children]
		# 调试
		# print("value :", max(children_value))
		return self.children[children_value.index(max(children_value))]

	# 对未完全展开的非叶节点进行展开
	def expand(self):
		position, move = self.all_child.pop()  # 探索为探索的子节点，并将其从未探索集合中删去
		next_state = self.state.update(position, move)
		child_node = MCTNode_2(next_state, parent=self)
		self.children.append(child_node)
		return child_node

	# 回溯更新
	def backpropagate(self, result):
		self._visit_num += 1
		if result == 1:
			self._wins_num += 1
		if self.parent:
			self.parent.backpropagate(result)

	# 判断叶节点
	def is_terminal_node(self):
		end_or_not = self.state.has_a_winner()[0]
		return end_or_not

	# 判断完全展开
	def is_fully_expanded(self):
		return len(self.all_child) == 0

	# 单次随机仿真, simulation
	def rollout(self, player):
		current_rollout_state = self.state
		while not current_rollout_state.has_a_winner()[0]:  # 单次仿真不断展开到叶节点为止
			possible_moves = current_rollout_state.acquirability  # 当前仿真节点合法移动步
			position, move = self.rollout_policy(possible_moves)  # 选择某个策略来确定某个合法移动步
			current_rollout_state = current_rollout_state.update(position, move)  # 进行合法移动步后的状态

		if current_rollout_state.has_a_winner()[1] == player:
			return 1
		else:
			return 0

	def rollout_policy(self, possible_moves):  # 随机选择一种可行的下法
		position, move = random.choice(list(possible_moves))
		return position, move


class MCTS_2(object):
	def __init__(self, node):
		self.root = node

	# 仿真后选出最佳行动

	def get_action(self):
		simulations_num = 300  # 修改搜索深度
		for i in range(simulations_num):
			v = self.tree_policy()
			reward = v.rollout(self.root.state.player)
			v.backpropagate(reward)

		return self.root.best_child(c_param=1.0)  # 更改value function

	# 选取叶节点（若非叶节点，进行展开）
	def tree_policy(self):
		current_node = self.root
		while not current_node.is_terminal_node():
			if current_node.is_fully_expanded():
				current_node = current_node.best_child()
			else:
				current_node = current_node.expand()
				return current_node
		return current_node

	def __str__(self):
		return "AI"
