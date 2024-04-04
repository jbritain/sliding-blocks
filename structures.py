def taxicab_distance(pos_1: tuple[int, int], pos_2: tuple[int, int]):
	return abs(pos_1[0] - pos_2[0]) + abs(pos_1[1] - pos_2[1])

class Block:
	def __init__(self, width: int, height: int, position: tuple[int, int], id: int = -1) -> None:
		self.width = width
		assert width > 0

		self.height = height
		assert height > 0

		self.position = position
		assert position[0] >= 0
		assert position[1] >= 0

		self.available_moves = None

		# positions we know we're blocked on, so we check these first when determining if we can move
		self.left_block_y = -1
		self.right_block_y = -1
		self.top_block_x = -1
		self.bottom_block_x = -1

	def __str__(self):
		return f"{self.width} {self.height} {self.position[0]} {self.position[1]}"
	
	def __eq__(self, other):
		if not isinstance(other, Block):
			raise NotImplementedError

		if self.width != other.width:
			#print("widths not equal")
			return False
		if self.height != other.height:
			#print("heights not equal")
			return False
		if self.position != other.position:
			#print(f"position not equal: {self.position}, {other.position}")
			return False
		#print("Equal!")
		return True
	
	def get_available_moves(self, board):
		if self.available_moves == None:
			self.available_moves = self.generate_available_moves(board)
		return self.available_moves
	
	def generate_available_moves(self, board):

		block_position = self.position

		occupied = board.get_occupied_spaces()

		moves = []

		#print(f"Checking block at {self.position}")
		for x_offset in range(-1, -block_position[0]-1, -1): # if we can move then we check another block in that direction to see how far we can go
			# check the left
			left_occupied = False
			#print(f"Checking left position {block_position[0]+x_offset}, {block_position[1]}: ", end="")
			if(self.left_block_y != -1 and occupied[self.left_block_y][block_position[0] + x_offset]): # check position we were blocked at last time since this is most likely to still be blocking us
					#print("cache hit - ", end="")
					left_occupied = True
			else:
					for i in range(self.height): # check all spaces one to the left of the block
							if occupied[block_position[1] + i][block_position[0] + x_offset]: # space is not empty
									left_occupied = True
									self.left_block_y = block_position[1] + i
									break

			if not left_occupied:
					#print("unoccupied")
					move = Move(self.position,(block_position[0] + x_offset, block_position[1]))
					moves.append(move)
			else:
					#print("occupied")
					break

		for y_offset in range(0, -block_position[1], -1):
			if (block_position[1] > 0): # ensure we aren't at the top of the board
					# check the top
					top_occupied = False
					#print(f"Checking top position {block_position[0]}, {block_position[1]+}: ", end="")
					if(self.top_block_x != -1 and occupied[block_position[1] - 1][self.top_block_x]): 
							#print("cache hit - ", end="")
							top_occupied = True
					else: 
							for i in range(self.width): # check all spaces one to the top of the block
									if occupied[block_position[1] - 1][block_position[0] + i]: # space is not empty
											top_occupied = True
											#self.top_block_x = block_position[0] + i
											break
					
					if not top_occupied:
							#print("unoccupied")
							move = Move(self.position, (block_position[0], block_position[1]-1))
							moves.append(move)
					else:
							#print("occupied")
							break

		if (block_position[0] + self.width < len(occupied[0]) - 1): # ensure we aren't at the right of the board
				# check the right
				right_occupied = False
				#print(f"Checking right position {block_position[0] + self.width}, {block_position[1]}: ", end="")
				if(self.right_block_y != -1 and occupied[self.right_block_y][block_position[0] + self.width]):
						#print("cache hit - ", end="")
						right_occupied = True
				else:
						for i in range(self.height): # check all spaces one to the right of the block
								if occupied[block_position[1] + i][block_position[0] + self.width]: # space is not empty
										right_occupied = True
										#self.right_block_y = block_position[1] + i
										break
				
				if not right_occupied:
						#print("unoccupied")
						move = Move(self.position, (block_position[0]+1, block_position[1]))
						moves.append(move)
				else:
						#print("occupied")
						pass

		if (block_position[1] + self.height < len(occupied) - 1): # ensure we aren't at the bottom of the board
				# check the bottom
				bottom_occupied = False
				#print(f"Checking bottom position {block_position[0]}, {block_position[1]+self.height}: ", end="")
				if(self.bottom_block_x != -1 and occupied[block_position[0]][self.bottom_block_x]):
						#print("cache hit - ", end="")
						bottom_occupied = True
				else:
						for i in range(self.width): # check all spaces one to the bottom of the block
								if occupied[block_position[1] + self.height][block_position[0] + i]: # space is not empty
										bottom_occupied = True
										#self.bottom_block_x = block_position[0] + i
										break
				
				if not bottom_occupied:
						#print("unoccupied")
						move = Move(self.position, (block_position[0], block_position[1]+1))
						moves.append(move)
				else:
						#print("occupied")
						pass

		if len(moves) == 0: # the self cannot move
				self.confirmed_cannot_move = True # store this in case we check it again

		return moves



class Move:
	def __init__(self, old_pos: tuple[int, int], new_pos: tuple[int, int]):
		self.old_pos = old_pos
		self.new_pos = new_pos

	def __str__(self):
		return f"{self.old_pos[0]} {self.old_pos[1]} {self.new_pos[0]} {self.new_pos[1]}"

class Board:
	def __init__(self, board: str, goals: str) -> None:
		parsed = Board.parse_board(board)
		self.blocks = parsed[1]
		self.length = parsed[0][0]
		self.width = parsed[0][1]
		
		self.goals = Board.parse_goals(goals)

	def __hash__(self):
		return hash((self.length, self.width, ' '.join([str(b) for b in self.blocks])))
    

	def parse_board(board: str) -> tuple[tuple[int, int], list[Block]]:
		'''
		Returns:
		tuple[tuple[int, int], list[Block]]: A tuple containing a tuple containing the width and height of the block, and a list of blocks on the board
		'''
		lines = board.split("\n")

		blocks = []

		first_line_split = lines[0].split(" ")
		
		length = int(first_line_split[0]) + 1
		assert length > 0

		width = int(first_line_split[1]) + 1
		assert width > 0

		for i, line in enumerate(lines[1:]): # skip first line as it describes the board
			line_split = line.split(" ")
			if(line == ''):
				continue
			blocks.append(Block(
				int(line_split[0]), 
				int(line_split[1]), 
				(
				int(line_split[2]), 
				int(line_split[3])
				),
				i + 1 # start at 1 since id 0 represents there not being a block
			))
			
		return ((length, width), blocks)

	def parse_goals(goals: str) -> list[Block]:
		goals_split = goals.split("\n")
		goal_blocks = []

		for goal in goals_split:
			if goal == '':
				continue
			goal_split = goal.replace("\n", "").split(" ")
			goal_blocks.append(Block(
				int(goal_split[0]), 
				int(goal_split[1]), 
				(
				int(goal_split[2]), 
				int(goal_split[3])
				)
			))
		
		return goal_blocks
	
	def is_solved(self) -> bool:
		for goal in self.goals:
			goal_found = False
			for block in self.blocks:
				if block == goal:
					goal_found = True
					#print("Matching block")
					break
			if not goal_found:
				#print("Goal not found")
				return False # we never found a block matching this goal
			
		#print("Solution match")	
		return True
	
	def make_move(self, move: Move) -> bool:
		move_made = False
		for block in self.blocks:
			block.available_moves = None

			if block.position == move.old_pos:
				block.position = move.new_pos
				block.left_block_y = -1
				block.right_block_y = -1
				block.top_block_x = -1
				block.bottom_block_x = -1
				move_made = True
			
		if move_made:
			return True
		
		raise Exception("No block could be found at the specified position")
	
	def __eq__(self, other):
		eq = True
		if self.width != other.width: return False
		if self.length != other.length: return False
		if self.blocks != other.blocks: return False
		if self.goals != other.goals: return False
		return eq
	
	# returns a value between 0 and 1 ranking how favourable the board is based on a number of factors
	def rank(self) -> float:
		# distance (taxicab)
		# we use taxicab since we can't move pieces diagonally

		# for each goal, select the nearest block which matches it, and use that distance
		# sum the distances

		distance_sum = 0

		for goal in self.goals:
			for block in self.blocks:
				if goal.width == block.width and goal.height == block.height: # matches goal
					distance = float('inf')
					taxicab = taxicab_distance(goal.position, block.position)
					distance = min(distance, taxicab) # set to smaller of two distances	
			
			distance_sum += distance

		goal_moves_blocked = 0
		# we want to be able to move the goal blocks closer to their goals
	 	# so prioritise moves which increase the amount of space around the goal blocks
		for goal in self.goals:
			for block in self.blocks:
				if goal.width == block.width and goal.height == block.height: # matches goal
					goal_moves_blocked += 4 - len(block.get_available_moves(self))
		

		return distance_sum + goal_moves_blocked
	
	def get_occupied_spaces(self) -> list[list[bool]]:
		occupied = [] # what blocks occupy what spaces
		for _ in range(self.width): # set all spaces to empty, an empty space has -1
				occupied.append([False] * self.length)

		for block in self.blocks:
				for y in range(block.height):
						for x in range(block.width):
								occupied[block.position[1] + y][block.position[0] + x] = True
		return occupied
	
		# gets all possible moves for a board
	def get_all_possible_moves(self) -> list[Move]:

			moves = []

			for block in self.blocks:
				moves.extend(block.get_available_moves(self))

			return moves

		


def moves_from_string(data: str) -> list[Move]:
	moves_split = data.split("\n")
	moves = []
	for move in moves_split:
		move_split = move.split(" ")
		moves.append(
			Move(
				(
					int(move_split[0]),
					int(move_split[1])
				),
				(
					int(move_split[2]),
					int(move_split[3])
				)
			)
		)
	return moves

class Queue:
	def __init__(self) -> None:
		self.queue = []

	def enqueue(self, e):
		self.queue.append(e)

	def dequeue(self):
		if len(self.queue) == 0:
			raise IndexError("Queue is empty")
		return self.queue.pop(0)
	
	def first(self):
		if len(self.queue) == 0:
			raise IndexError("Queue is empty")
		return self.queue[0]
	
	def __len__(self):
		return len(self.queue)