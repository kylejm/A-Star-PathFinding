'''
A-Star Path Finding Program

Description:
This program creates a 30 by 30 grid in pygame where the user can place two nodes (orange as start and blue as end)
with barriers in bewteen. The route with the least amount of nodes is found using the A-Star algorithm.

Algorithm:
A-Star path finding is an informed search algorithm which means we cconsider the endpoint location but we do not 
know intially where the barriers / walls are. In the search we will check the nearest neighbors on the 2D plane which
means the nodes adjacent to the start node. Then we use the prioroty score of each node to determine the quickest route 
searching. The equation of this function is f(n) = g(n) + h(n) where f(n) is the priority score of n (node), g(n) is the
current shortest distance and h(n) is the estimate distance from n to the end. For this 2D plane, we assume that each node
has an edge of score 1.

This program was written along with the youtube video linked below
https://www.youtube.com/watch?v=JtiK0DOeI4A

Some changes were made to this program including
 - usage of pygame grid derivered from my "Drawing with Pygame" github 
 - complete comment of algorithm and code
 - reconstructed main function
 - added print statement in terminal to check how many nodes it took to get from end to start

'''

import pygame
from queue import PriorityQueue

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = [] # list of nearest neighbors 
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def looked(self):
		return self.color == RED
		# already looked at the node

	def wall(self):
		return self.color == BLACK
		# mouse drawn barrier node

	def is_start(self):
		return self.color == ORANGE
		# mouse placed start node

	def is_end(self):
		return self.color == TURQUOISE
		# mouse placed end node

	def reset(self):
		self.color = WHITE
		# reset to norm

	def make_start(self):
		self.color = ORANGE

	def make_looked(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_wall(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	# Updating neighbors in the open set
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].wall(): # look at neighbor below
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].wall(): # look at neighbor above
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].wall(): # look at neighbor to the right
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].wall(): # look at neighbor to the left
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# Heuristic function
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Construct the path of fastest route from end to start 
def reconstruct_path(came_from, current, draw):
	count = 0
	while current in came_from:
		current = came_from[current]
		current.make_path()
		count += 1
		draw()
	print(f'The number of nodes it took for A-Star to get from end to start was {count} nodes')

# A-Star Algorithm 
def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() # returns queue of lowest value into open set
	open_set.put((0, count, start))
	came_from = {}

	# each g score and f score are considered infinite until changed by neighbors
	g_score = {spot: float("inf") for row in grid for spot in row} 
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	# Quit Program
	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		# Reconstruct path
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		# Assuming each edge is 1, the g score is at least 1 away
		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			# calculating f score
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

				# addd neighbot into open set 
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()

		if current != start:
			current.make_looked()

	return False

# Creating Grid lines Vert and Horz
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Node(i, j, gap, rows)
			grid[i].append(spot)

	return grid

# Grid display and update
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

# Return position of mouse when clicked
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

if __name__ == "__main__":

	# Pygame Display setting 
	pygame.display.set_caption("A-Star Path Finding Algorithm written by Kyle Massie")
	width = 800
	win = pygame.display.set_mode((width, width))
	rows = 30
	grid = make_grid(rows, width)

	start = None
	end = None
	run = True


	while run:
		draw(win, grid, rows, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_wall()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, rows, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(rows, width)

	pygame.quit()