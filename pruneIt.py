import sys

max_val = sys.maxint
min_val = -sys.maxint - 1

class Player(object):

	def __init__(self, id, preferenceLine):
		self.id = id
		self.preference = {}
		# self.score = 0

		for pair in preferenceLine.split(', '):
			dataList = pair.split(': ')
			self.preference[dataList[0]] = int(dataList[1])

	# def add_node_score(self, node):
	# 	self.score += self.preference[node.color]


class Node(object):

	def __init__(self, name):
		self.name = name
		self.color = None
		self.owner = None
		self.parent = None
		self.neighbors = []
		self.score = 0

	def occupy(self, player, color):
		self.owner = player
		self.color = color
		# print 'player ' + str(player.id),
		# print ' visiting ' + self.name + ' color: ' + color

	def free(self):
		self.color = None
		self.owner = None
		self.score = 0

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
max_depth = 0

def print_graph():
	for node_name, node in graph.items():
		node = graph[node_name]

		neighbors = node.name + ' :'
		for neighbor in node.neighbors:
			neighbors += ' ' + neighbor.name

		if node.owner:
			neighbors += ' owned by player' + str(node.owner.id) + ' color: ' + node.color
		print neighbors


# def get_score(leaf):

# 	players[1].score = 0
# 	players[2].score = 0

# 	for node_name, node in graph.items():
# 		if node.owner:
# 			node.owner.add_node_score(node)

# 	# print 'player1: ' + str(players[1].score)
# 	# print 'player2: ' + str(players[2].score)
# 	score = players[1].score-players[2].score
# 	# print 'counter ' + str(counter)
# 	# print 'score ' + str(score)

# 	if score == 12:
# 		while leaf:
# 			leaf.info()
# 			leaf = leaf.parent

def print_log(node, depth, value, a, b):
	print ', '.join([node.name, node.color, str(depth), str(value), str(a), str(b)])


def find_best_move(visited, frontier, playerId, a, b, depth):

	if depth > max_depth:
		return None

	player = players[playerId]
	sorted_frontier = list(frontier)
	sorted_frontier.sort(key=lambda n: n.name)
	# print '\nstep ' + str(step),
	# print ' player' + str(playerId) + ' turn'
	# print 'frontier'
	# for node in sorted_frontier:
	# 	print node.name,
	# print ''
	# cant_color_any_node = True
	best_node = None
	best_color = None
	val = '-inf'
	if player.id == 2:
		val = 'inf'

	for node in sorted_frontier:
		
		# find available colors for this node
		non_adjacent_colors = set(colors)
		for neighbor in node.neighbors:
			if neighbor.color:
				non_adjacent_colors.discard(neighbor.color)
		sorted_non_adjacent_colors = list(non_adjacent_colors)
		sorted_non_adjacent_colors.sort()

		visited.add(node)
		frontier.remove(node)
		for color in sorted_non_adjacent_colors:

			point = player.preference[color]
			if player.id==2:
				point = -point

			node.occupy(player, color)
			# print_log(node, depth, v, a, b)

			# print 'point ' + str(point)
			# if depth == max_depth:
			# 	val = point

			print_log(node, depth, val, a, b)
			new_neighbors = set()
			for neighbor in node.neighbors:
				if (neighbor not in frontier) and (neighbor not in visited):
					new_neighbors.add(neighbor)
			frontier.update(new_neighbors)
			# frontier.discard(node)


			next_node = find_best_move(visited, frontier, playerId%2+1, a, b, depth+1)
			score = 0
			if next_node: 
				score = next_node.score
			
			# node.score = score
			
			# if score > max_score:
			# 	max_score = score
			# 	best_node = node
			# 	best_color = color
			score += point




			if player.id == 1:
				# score += point
				if val == '-inf' or score > val:
					val = score
					best_node = node
					best_color = color
					a = max(a, val)
					# print_log(node, depth, val, a, b)

			else:
				# score -= point
				if val=='inf' or score < val:
					val = score
					best_node = node
					best_color = color
					b = min(b, val)
					# print_log(node, depth, val, a, b)


			# unvisit node, remove added nodes in frontier
			frontier.difference_update(new_neighbors)
			
			node.free()
			node.parent = None
			# if b <= a:
			# 	break

		visited.remove(node)
		frontier.add(node)


	if best_node:
		best_node.occupy(player, best_color)
		best_node.score = val
		# print 'step ' + str(step),
		# print ' best choice: ' + best_node.name + ' score: ' + str(val)
		# print ''
		# print ''
		# print ''
		# print ''
	# else:
	# 	print 'no choice available'
	

	# if cant_color_any_node:
	# 	counter = counter + 1
	# 	print '===========cant_color_any_node=============='
	# 	return get_score(parent)
	
	return best_node

with open("testcases/t5.txt", 'r') as f:

	lines = f.read().split('\n')
	colors = lines[0].strip().split(', ')
	colors.sort()
	max_depth = int(lines[2].strip())

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

	parent = None
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

		parent = node



	frontier -= visited

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
	print_log(parent, 0, '-inf', '-inf', 'inf')
	best_first_move = find_best_move(visited, frontier, 2, '-inf', 'inf', 1)

	print best_first_move.name , 
	print best_first_move.color ,
	print best_first_move.score + initial_score











