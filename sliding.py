import sys

from structures import *
from solver import *

board_path = None
goal_path = None


board_path = sys.argv[1]
goal_path = sys.argv[2]


with open(board_path) as bf:
	
	board_data = bf.read()

	with open(goal_path) as gf:
		goal_data = gf.read()

	board = board_from_string(board_data, goal_data)
	board_copy = copy.deepcopy(board)
	solution = solve(board)

	if(solution == []):
		print("-1")
	else:
		for move in solution:
			print(move)
