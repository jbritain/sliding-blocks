class Block:
	def __init__(self, width: int, height: int, position: tuple[int, int]) -> None:
		self.width = width
		assert width > 0

		self.height = height
		assert height > 0

		self.position = position
		assert position[0] >= 0
		assert position[1] >= 0
	
	def __eq__(self, other):
		if not isinstance(other, Block):
			return NotImplemented

		return (
			self.width    == other.width  and
			self.height   == other.height and
			self.position == other.position
		)

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
			if not goal_found:
				return False # we never found a block matching this goal
		
		return True
	
	def make_move(self, move: Move) -> bool:
		for block in self.blocks:
			if block.position == move.old_pos:
				block.position = move.new_pos
				return True
		
		return False
	
	def __eq__(self, other):
		eq = True
		if self.width != other.width: return False
		if self.length != other.length: return False
		if self.blocks != other.blocks: return False
		if self.goals != other.goals: return False

		