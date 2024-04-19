from .vec import vec2
from .block import Block, all_ones
from .move import Move
import copy

def set_bit(val, bit):
	return val | (1<<bit)

def unset_bit(val, bit):
	return val & ~(1<<bit)

class Board:
	# blocks and goals are lists of blocks
	def __init__(self, width, length, blocks, goals, big_tray):
		self.size = vec2(width, length)
		self.blocks = blocks
		self.goals = goals
		self.rank_val = None
		self.occupied_vert = None
		self.occupied_hor = None
		self.hash = None
		self.moves_made = []
		self.big_tray = big_tray # case: the board is all 1x1 blocks and has one free space
		if self.big_tray: # the target empty position for a big tray
			self.big_tray_gap = self.find_gap(True)

	@property
	def height(self):
		return self.size.y

	@property
	def width(self):
		return self.size.x

	def generate_rank(self):
		# distance (taxicab)
		# we use taxicab since we can't move pieces diagonally

		# for each goal, select the nearest block which matches it, and use that distance
		# sum the distances

		distance_sum = sum(b.get_goal_distance(self) for b in self.blocks)

		# goal_moves_blocked = 0
		# # we want to be able to move the goal blocks closer to their goals
	 	# # so prioritise moves which increase the amount of space around the goal blocks
		# for goal in self.goals:
		# 	for block in self.blocks:
		# 		if goal.width == block.width and goal.height == block.height: # matches goal
		# 			goal_moves_blocked += len(block.get_available_moves(self))
		

		return distance_sum # + goal_moves_blocked

	# returns the board ranking, only recalculating if necessary
	@property
	def rank(self): 
		if self.rank_val is None:
			self.rank_val = self.generate_rank()
		return self.rank_val
	
	def is_solved(self):
		if self.big_tray:
			return self.find_gap() == self.big_tray_gap

		for goal in self.goals:
			found_goal = False
			for block in self.blocks:
				if goal == block:
					found_goal = True
					break
			if not found_goal:
				return False
		return True
	
	# if chbit is true, the bitboard is modified. Should only be False if we know we are immediately going to undo the move
	# if count_move is true, the move is added to the moves_made list. Should be false if we are undoing a move and thus removing it from moves_made
	def make_move(self, move, chbit=True, count_move=False):
		move_made = False
		for block in self.blocks:
			block.available_moves = None
			if not move_made and block.position == move.old_pos:
				block.position = move.new_pos
				block.goal_distance_val = None
				# self.occupied_hor = None
				# self.occupied_vert = None
	
				if count_move:
					self.moves_made.append(move)


				if chbit and self.occupied_hor and self.occupied_vert:
					for x in range(block.size.x):
						for y in range(block.size.y):
							old_x = move.old_pos.x + x
							old_y = move.old_pos.y + y
							
							self.occupied_vert[old_x] = unset_bit(self.occupied_vert[old_x], self.size.y - (old_y) - 1)
							self.occupied_hor[old_y] = unset_bit(self.occupied_hor[old_y], self.size.x - (old_x) - 1)
							

					for x in range(block.size.x):
						for y in range(block.size.y):
							new_x = move.new_pos.x + x
							new_y = move.new_pos.y + y

							self.occupied_vert[new_x] = set_bit(self.occupied_vert[new_x], self.size.y - (new_y) - 1)
							self.occupied_hor[new_y] = set_bit(self.occupied_hor[new_y], self.size.x - (new_x) - 1)

				self.rank_val = None
				move_made = True
				self.hash = None
		if move_made:
			return
		raise Exception("Block not found")
	
	# LEGACY METHOD, DOESN'T REMOVE FROM moves_made, DON'T CALL EXTERNALLY (use undo_last)
	def undo_move(self, move, chbit=True):
		if chbit == True:
			pass
		inverse_move = Move(move.new_pos, move.movement * -1)
		return self.make_move(inverse_move, chbit)
	
	# ONLY CALL IF THE LAST MOVE WE MADE WAS ONE WE COUNTED
	def undo_last(self):
		last_move = self.moves_made.pop()
		return self.undo_move(last_move, True)
	
	def find_gap(self, goal=False):
		gap_row = -2
		gap_col = -2

		if goal:
			rows = self.generate_occupied(False, goal)
			cols = self.generate_occupied(True, goal)
		else:
			rows = self.get_occupied(False)
			cols = self.get_occupied(True)
		for y, row in enumerate(rows):
			if not all_ones(row) or row.bit_length() != self.width:
				gap_row = y
				break
		for x, col in enumerate(cols):
			if not all_ones(col) or col.bit_length() != self.height:
				gap_col = x
				break
		
		return vec2(gap_col, gap_row)
	
	
	# if vertical is false, we generate for horizontal
	# returns an array of binary numbers representing a row on the board
	# a 1 is an occupied space, a 0 is an empty one
	def generate_occupied(self, vertical, goal=False):
		if goal:
			blocks = self.goals
		else:
			blocks = self.blocks

		if vertical:
			cols = [0] * self.size.x
			
			for block in blocks:
				for x in range(block.size.x):
					for y in range(block.size.y):
						x_pos = block.position.x + x
						cols[x_pos] = set_bit(cols[x_pos], self.size.y - (block.position.y + y) - 1)
			 
			return cols
		
		rows = [0] * self.size.y

		for block in blocks:
			for x in range(block.size.x):
				for y in range(block.size.y):
					y_pos = block.position.y + y
					rows[y_pos] = set_bit(rows[y_pos], self.size.x - (block.position.x + x) - 1)

		return rows

	def get_occupied(self, vertical):
		if vertical:
			if self.occupied_vert is None:
				self.occupied_vert = self.generate_occupied(True)
			return self.occupied_vert
		
		if self.occupied_hor is None:
			self.occupied_hor = self.generate_occupied(False)
		return self.occupied_hor


	def visualise(self, goal=False):
		chars = [
			"■",
			"□",
			"▣",
			"▤",
			"▥",
			"▦",
			"▧",
			"▨",
			"▩",
		]

		vis = []
		for _ in range(self.size.y):
			vis.append(["  "] * self.size.x)

		items = self.goals if goal else self.blocks

		for i, block in enumerate(items):
			char = chars[i % (len(chars) - 1)] + " "

			for y in range(block.size.y):
				for x in range(block.size.x):
					vis[block.position.y + y][block.position.x + x] = char

		full_vis = ""
		full_vis += "┌" + "─" * ((self.size.x) * 2) + "┐\n"
		for row in vis:
			full_vis += f"│{''.join(row)}│\n"
		full_vis += "└" + "─" * ((self.size.x) * 2) + "┘"
		

		print(full_vis)
		if not goal:
			#print(f"HASH: {hash(self)}")

			if self.occupied_vert and self.occupied_hor:
				print("vert")
				for v in self.occupied_vert:
					print(bin(v))
				print("hor")
				for h in self.occupied_hor:
					print(bin(h))

	def __eq__(self, other):
		return hash(self) == hash(other)
	
	
	def __hash__(self):
		if self.hash is None:
			norm = sorted((block.position.y, block.position.x, block.size.y, block.size.x) for block in self.blocks)
			self.hash = hash(tuple(norm))
		return self.hash
	
	def __deepcopy__(self, memo):
		new_block_array = []
		for block in self.blocks:
			new_block_array.append(copy.deepcopy(block))
		return Board(self.size.x, self.size.y, new_block_array, self.goals, self.big_tray)


def board_from_string(board_string, goal_string):
	# set up the board
	board_lines = [l for l in board_string.split("\n") if l]
	dims = board_lines[0].split(" ")
	length = int(dims[0])
	width = int(dims[1])

	blocks = []

	big_tray = len(board_lines) == (width * length)
	
	for line in board_lines[1:]:
		data = line.split(" ")
		block = Block(int(data[0]), int(data[1]), int(data[2]), int(data[3]))
		if (not big_tray) or (not block.width == block.height == 1):
			big_tray = False
		blocks.append(block)

	#if big_tray: print("big tray")

	goal_lines = goal_string.split("\n")

	goals = []
	for line in goal_lines:
		if line:
			data = line.split(" ")
			goals.append(Block(int(data[0]), int(data[1]), int(data[2]), int(data[3])))

	return Board(width, length, blocks, goals, big_tray)