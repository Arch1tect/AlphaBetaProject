import sys

max_val = sys.maxint
min_val = -sys.maxint - 1

class Player(object):

	def __init__(self, id, preferenceLine):
		self.id = id
		self.preference = {}

		for pair in preferenceLine.split(', '):
			dataList = pair.split(': ')
			self.preference[dataList[0]] = int(dataList[1])

	def get_point(self, color):
		point = self.preference[color]
		if self.id == 2:
			point = -point
		return point


class Node(object):

	def __init__(self, name):
		self.name = name
		self.color = None
		self.owner = None
		self.is_max_node = None
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

graph = {}
players = {}
colors = []
counter = 1
max_depth = 0
first_next_node_name = ''
first_next_node_color = ''

def print_graph():
	for node_name, node in graph.items():
		node = graph[node_name]

		neighbors = node.name + ' :'
		for neighbor in node.neighbors:
			neighbors += ' ' + neighbor.name

		if node.owner:
			neighbors += ' owned by player' + str(node.owner.id) + ' color: ' + node.color
		print neighbors

def max_min_to_str(val):
	if val == max_val:
		return 'inf'
	if val == min_val:
		return '-inf'
	return val

def print_log(node, depth, value, a, b):

	value = max_min_to_str(value)
	a = max_min_to_str(a)
	b = max_min_to_str(b)
	print ', '.join([node.name, node.color, str(depth), str(value), str(a), str(b)])


def find_best_move(node, depth, score_so_far, visited, frontier, a, b):
	
	node_value = 0
	if depth % 2 == 0:
		node_value = min_val
	else:
		node_value = max_val

	sorted_frontier = list(frontier)
	sorted_frontier.sort(key=lambda n: n.name)

	# look ahead
	has_option = False
	for next_node in sorted_frontier:
		
		# find available colors for this node
		non_adjacent_colors = set(colors)
		for neighbor in next_node.neighbors:
			if neighbor.color:
				non_adjacent_colors.discard(neighbor.color)
		
		if len(non_adjacent_colors) > 0:
			has_option = True
			break

	if depth == max_depth or not has_option:
		node_value = score_so_far


	print_log(node, depth, node_value, a, b)


	if depth == max_depth or not has_option:
		return score_so_far



	# Now we look into what move to take next

	next_player = players[node.owner.id%2+1]
	next_node_value = 0

	if depth % 2 == 0:
		# node.is_max_node 
		next_node_value = min_val
	else:
		next_node_value = max_val


	# best_node = None
	# best_color = None
	should_break = False


	for next_node in sorted_frontier:
		
		# find available colors for this node
		non_adjacent_colors = set(colors)
		for neighbor in next_node.neighbors:
			if neighbor.color:
				non_adjacent_colors.discard(neighbor.color)
		sorted_non_adjacent_colors = list(non_adjacent_colors)
		sorted_non_adjacent_colors.sort()

		visited.add(next_node)
		frontier.remove(next_node)
		
		for color in sorted_non_adjacent_colors:

			point = next_player.get_point(color)

			next_node.occupy(next_player, color)

			new_neighbors = set()
			for neighbor in next_node.neighbors:
				if (neighbor not in frontier) and (neighbor not in visited):
					new_neighbors.add(neighbor)
			frontier.update(new_neighbors)

			score = find_best_move(next_node, depth+1, score_so_far+point, visited, frontier, a, b)

			if depth % 2 == 0:
				if score > next_node_value:
					next_node_value = score
					if depth == 0: 
						global first_next_node_name
						global first_next_node_color
						# print 'first_next_node_name'
						# print first_next_node_name
						first_next_node_name = next_node.name
						first_next_node_color = color

				if next_node_value < b:
					a = max(a, next_node_value)
				else:
					should_break = True

			else:

				next_node_value = min(next_node_value, score)
				if next_node_value > a:
					b = min(b, next_node_value)
				else:
					should_break = True

			print_log(node, depth, next_node_value, a, b)


			# unvisit node, remove added nodes in frontier
			frontier.difference_update(new_neighbors)
			next_node.free()

			if should_break:
				break

		visited.remove(next_node)
		frontier.add(next_node)
		if should_break:
			break
	return next_node_value

with open("testcases/t22.txt", 'r') as f:

	lines = f.read().split('\n')
	colors = lines[0].strip().split(',')
	colors = [color.strip() for color in colors]
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

	# print colors
	# print players[1].preference
	# print players[2].preference
	# print_graph()
	# print 'visited',
	# for visitedNode in visited:
	# 	print ' ' + visitedNode.name,

	# print '\nfrontier',
	# for frontierNode in frontier:
	# 	print ' ' + frontierNode.name,


	print '\n========find best move====================================='
	# print_log(parent, 0, '-inf', '-inf', 'inf')

	score = find_best_move(parent, 0, initial_score, visited, frontier, min_val, max_val)
	print ", ".join([first_next_node_name, first_next_node_color, str(score)])












