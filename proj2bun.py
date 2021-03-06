import sys

class Player(object):

	def __init__(self, id, preferenceLine):
		self.id = id
		self.preference = {}
		self.score = 0

		for pair in preferenceLine.split(', '):
			dataList = pair.split(': ')
			self.preference[dataList[0]] = int(dataList[1])

	def add_node_score(self, node):
		self.score += self.preference[node.color]


class Node(object):

	def __init__(self, name):
		self.name = name
		self.color = None
		self.owner = None
		self.parent = None
		self.neighbors = []
		self.score = None

	def occupy(self, player, color):
		self.owner = player
		self.color = color
		# print 'visiting ' + self.name + ' color: ' + color

	def free(self):
		self.color = None
		self.owner = None

	def info(self):
		print ' '.join([self.name, self.color, str(self.owner.id)])

	def add_neighbors(self, neighbors, graph):
		for neighbor in neighbors:
			neighborNode = None
			if neighbor in graph:
				neighborNode = graph[neighbor]
			else:
				neighborNode = Node(neighbor)
				graph[neighbor] = neighborNode

			self.neighbors.append(neighborNode)
		# self.neighbors.sort(key=lambda n: n.name)

graph = {}
players = {}
colors = []
counter = 1

def print_graph():
	for node_name, node in graph.items():
		node = graph[node_name]

		neighbors = node.name + ' :'
		for neighbor in node.neighbors:
			neighbors += ' ' + neighbor.name

		if node.owner:
			neighbors += ' owned by player' + str(node.owner.id) + ' color: ' + node.color
		print neighbors


def get_score(leaf):

	players[1].score = 0
	players[2].score = 0

	for node_name, node in graph.items():
		if node.owner:
			node.owner.add_node_score(node)

	# print 'player1: ' + str(players[1].score)
	# print 'player2: ' + str(players[2].score)
	score = players[1].score-players[2].score
	# print 'counter ' + str(counter)
	# print 'score ' + str(score)

	if score == 12:
		while leaf:
			leaf.info()
			leaf = leaf.parent



def find_best_move(parent, frontier, playerId):

	# global counter
	# if len(frontier) == 0:
		
	# 	# print 'all visited: ' + str(counter)
	# 	counter = counter + 1
		
	# 	return None

	player = players[playerId]
	sorted_frontier = list(frontier)
	sorted_frontier.sort(key=lambda n: n.name)
	
	# print 'player' + str(playerId) + ' turn'

	# print 'frontier'
	# for node in sorted_frontier:
	# 	print node.name,
	# print ''
	# cant_color_any_node = True
	bestNode = None
	bestColor = None
	max_score = -sys.maxint - 1
	for node in sorted_frontier:
		
		if node.owner:
			continue
		# find available colors for this node
		non_adjacent_colors = set(colors)
		for neighbor in node.neighbors:
			if neighbor.color:
				non_adjacent_colors.discard(neighbor.color)
		sorted_non_adjacent_colors = list(non_adjacent_colors)
		sorted_non_adjacent_colors.sort()
		# print 'sorted_non_adjacent_colors'
		# print sorted_non_adjacent_colors

		frontier.remove(node)
		for color in sorted_non_adjacent_colors:

			# cant_color_any_node = False
			# print 'color' + color


			score = player.preference[color]
			node.occupy(player, color)
			node.parent = parent
			new_neighbors = set()
			for neighbor in node.neighbors:
				if neighbor not in frontier and not neighbor.owner:
					new_neighbors.add(neighbor)
			frontier.update(new_neighbors)
			next_node = find_best_move(node, frontier, playerId%2+1)
			
			if next_node:
				score -= next_node.score
			node.score = score
			if score > max_score:
				max_score = score
				bestNode = node
				bestColor = color

			# unvisit node 
			frontier.difference_update(new_neighbors)
			node.free()
			node.parent = None

		frontier.add(node)


	if bestNode:
		bestNode.score = score
		bestNode.color = bestColor
		# print 'best choice: ' + bestNode.name + ' score: ' + str(max_score)
	# else:
	# 	print 'no choice available'
	

	# if cant_color_any_node:
	# 	counter = counter + 1
	# 	print '===========cant_color_any_node=============='
	# 	return get_score(parent)
	
	return bestNode

with open("testcases/t5.txt", 'r') as f:

	lines = f.read().split('\n')
	colors = lines[0].strip().split(', ')
	colors.sort()
	depth = int(lines[2].strip())

	# parse player preference
	
	players[1] = Player(1, lines[3].strip())
	players[2] = Player(2, lines[4].strip())

	
	# parse adjacency list and build graph
	for line in lines[5:-1]:
		data = line.strip().split(': ')
		node_name = data[0]
		node = None
		if node_name in graph:
			node = graph[node_name]
		else:
			node = Node(node_name)
			graph[node_name] = node
		neighbors = data[1].split(', ')
		node.add_neighbors(neighbors, graph)

	frontier = set()
	visited = set()
	# parse initial state
	initial_states = lines[1].strip().split(', ')
	initial_score = 0
	for state in initial_states:
		data = state.split(': ')
		node = graph[data[0]]
		state_info = data[1].split('-')
		player = players[int(state_info[1])]
		color = state_info[0]
		node.occupy(player, color)
		point = player.preference[color]
		if player.id == 1:
			initial_score += point
		else:
			initial_score -= point
		visited.add(node)
		frontier.update(node.neighbors)

	frontier -= visited

	# check if input parsed correctly, remove when submit
	print colors
	print players[1].preference
	print players[2].preference
	print_graph()
	print 'visited',
	for visitedNode in visited:
		print ' ' + visitedNode.name,

	print '\nfrontier',
	for frontierNode in frontier:
		print ' ' + frontierNode.name,

	print '\n========find best move====================================='
	best_first_move = find_best_move(None, frontier, 1)

	print best_first_move.name
	print best_first_move.color
	print best_first_move.score + initial_score











