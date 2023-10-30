import sys
import numpy as np
import random


class Node:
	def __init__(self, state, parent, action, cost = 0, h=0):
		self.state = state
		self.parent = parent
		self.action = action
		self.cost = cost
		if(parent is not None):
			self.cost += parent.cost
		self.f = self.cost + h



class StackFrontier:
	def __init__(self):
		self.frontier = []

	def add(self, node):
		self.frontier.append(node)

	def contains_state(self, state):
		return any((node.state[0] == state[0]).all() for node in self.frontier)
	
	def empty(self):
		return len(self.frontier) == 0
	
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[-1]
			self.frontier = self.frontier[:-1]
			return node


class QueueFrontier(StackFrontier):
	def remove(self):
		if self.empty():
			raise Exception("Empty Frontier")
		else:
			node = self.frontier[0]
			self.frontier = self.frontier[1:]
			return node


class Puzzle:
	def __init__(self, start, startIndex, goal, goalIndex, max_cost = 5, size=3):
		self.start = [start, startIndex]
		self.goal = [goal, goalIndex] 
		self.solution = None
		self.num_explored = 0
		self.max_cost = max_cost
		self.puzzle_size = size

	def neighbors(self, state, shuffle = True):
		mat, (row, col) = state
		results = []
		
		if row > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row - 1][col]
			mat1[row - 1][col] = 0
			results.append(('up', [mat1, (row - 1, col)]))
		if col > 0:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col - 1]
			mat1[row][col - 1] = 0
			results.append(('left', [mat1, (row, col - 1)]))
		if row < self.puzzle_size - 1:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row + 1][col]
			mat1[row + 1][col] = 0
			results.append(('down', [mat1, (row + 1, col)]))
		if col < self.puzzle_size - 1:
			mat1 = np.copy(mat)
			mat1[row][col] = mat1[row][col + 1]
			mat1[row][col + 1] = 0
			results.append(('right', [mat1, (row, col + 1)]))

		if(shuffle):
			random.shuffle(results)
		return results

	def print(self):
		solution = self.solution if self.solution is not None else None
		print("Start State:\n", self.start[0], "\n")
		print("Goal State:\n",  self.goal[0], "\n")
		print("\nStates Explored: ", self.num_explored, "\n")
		print("Solution:\n ")
		for action, cell in zip(solution[0], solution[1]):
			print("action: ", action, "\n", cell[0], "\n")
		print("Goal Reached!!")

	def does_not_contain_state(self, state):
		for st in self.explored:
			if (st[0] == state[0]).all():
				return False
		return True
	
	# get the Heuristic value by comparing the number of error tiles between
	# a state and the goal state
	def getHeuristic(self, state):
		heuristic = 0
		goal = self.goal[0]
		for r in range(self.puzzle_size):
				for c in range(self.puzzle_size):
					if(state[r][c] != goal[r][c] and state[r][c] != 0):
						heuristic += 1
		return heuristic

	def BFSsolve(self):
		self.num_explored = 0

		start = Node(state=self.start, parent=None, action=None)
		frontier = QueueFrontier()
		frontier.add(start)

		self.explored = [] 

		while True:
			if frontier.empty():
				# raise Exception("No solution")
				self.solution = None
				break

			node = frontier.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			for action, state in self.neighbors(node.state):
				if not frontier.contains_state(state) and self.does_not_contain_state(state):
					child = Node(state=state, parent=node, action=action)
					frontier.add(child)

	def DFSsolve(self):
		self.num_explored = 0
		start = Node(state=self.start, parent=None, action=None, cost=0)
		frontier = StackFrontier()
		frontier.add(start)

		move_cost = 1
		self.explored = [] 

		while True:
			if frontier.empty():
				# raise Exception("No solution")
				break

			node = frontier.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			if(node.cost < self.max_cost):
				for action, state in self.neighbors(node.state):
					if not frontier.contains_state(state) and self.does_not_contain_state(state):
						child = Node(state=state, parent=node, action=action, cost=move_cost)
						frontier.add(child)

	def A_solve(self):
		self.num_explored = 0
		start = Node(state=self.start, parent=None, action=None, cost=0,h=self.getHeuristic(self.start[0]))
		frontier = StackFrontier()
		frontier.add(start)

		move_cost = 1
		self.explored = []

		while True:
			if frontier.empty():
				# raise Exception("No solution")
				break

			node = frontier.remove()
			self.num_explored += 1

			if (node.state[0] == self.goal[0]).all():
				actions = []
				cells = []
				while node.parent is not None:
					actions.append(node.action)
					cells.append(node.state)
					node = node.parent
				actions.reverse()
				cells.reverse()
				self.solution = (actions,  cells)
				return

			self.explored.append(node.state)

			childs = []
			for action, state in self.neighbors(node.state, shuffle=False):
				if not frontier.contains_state(state) and self.does_not_contain_state(state):
						child = Node(state=state, parent=node, action=action, cost=move_cost, h=self.getHeuristic(state[0]))
						# frontier.add(child)
						childs.append(child)

			#store only childs with the minimum f value in frontier
			if(len(childs) > 0):
				min_f = childs[0].f
				for child in childs:
					if(min_f > child.f):
						min_f = child.f
				for child in childs:
					if(child.f == min_f):
						frontier.add(child)

			frontier.frontier.sort(reverse=True, key=lambda x:x.f)
