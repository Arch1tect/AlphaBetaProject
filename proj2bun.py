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
		self.neighbors = []

	def occupy(self, player, color):
		self.owner = player
		self.color = color
		# print 'visiting ' + self.name

	def free(self):
		self.color = None
		self.owner = None

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


def get_score():

	players[1].score = 0
	players[2].score = 0

	for node_name, node in graph.items():
		if node.owner:
			node.owner.add_node_score(node)

	print 'player1: ' + str(players[1].score)
	print 'player2: ' + str(players[2].score)


def find_best_move(frontier, playerId):

	if len(frontier) == 0:
		global counter
		print 'all visited: ' + str(counter)
		counter = counter + 1
		get_score()

	player = players[playerId]
	sorted_frontier = list(frontier)
	sorted_frontier.sort(key=lambda n: n.name)
	# print playerId

	# print 'frontier'
	# for node in sorted_frontier:
	# 	print node.name,
	# print ''

	for node in sorted_frontier:
		frontier.remove(node)
		non_adjacent_colors = set(colors)
		for neighbor in node.neighbors:
			if neighbor.color:
				non_adjacent_colors.discard(neighbor.color)
		sorted_non_adjacent_colors = list(non_adjacent_colors)
		sorted_non_adjacent_colors.sort()

		for color in non_adjacent_colors:

			node.occupy(player, color)
			new_neighbors = set()
			for neighbor in node.neighbors:
				if neighbor not in frontier and not neighbor.owner:
					new_neighbors.add(neighbor)
			frontier.update(new_neighbors)
			find_best_move(frontier, playerId%2+1)
			frontier.difference_update(new_neighbors)
			node.free()
		frontier.add(node)



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
	for state in initial_states:
		data = state.split(': ')
		node = graph[data[0]]
		state_info = data[1].split('-')
		node.occupy(players[int(state_info[1])], state_info[0])
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
	find_best_move(frontier, 1)











