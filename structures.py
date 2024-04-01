class Block:
	def __init__(self, width: int, height: int, position: tuple[int, int]) -> None:
		self.width = width
		assert width > 0

		self.height = height
		assert height > 0

		self.position = position
		assert position[0] >= 0
		assert position[1] >= 0

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

		for line in lines[1:]: # skip first line as it describes the board
			line_split = line.split(" ")
			if(line == ''):
				continue
			blocks.append(Block(
				int(line_split[0]), 
				int(line_split[1]), 
				(
				int(line_split[2]), 
				int(line_split[3])
				)
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
		for block in self.blocks:
			if block.position == move.old_pos:
				block.position = move.new_pos
				return True
		
		raise Exception("No block could be found at the specified position")
	
	def __eq__(self, other):
		eq = True
		if self.width != other.width: return False
		if self.length != other.length: return False
		if self.blocks != other.blocks: return False
		if self.goals != other.goals: return False
		return eq

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