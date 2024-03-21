import sys
import os

os.system("cls")

from structures import *
from solve_checker import *
from solver import *

board_path = sys.argv[1]
goal_path = sys.argv[2]

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

with open(board_path) as bf:
	board_data = bf.read()

with open(goal_path) as gf:
	goal_data = gf.read()

board = Board(board_data, goal_data)

# print("BOARD:")
# print(visualise_board(board))

# print("GOAL:")
# print(visualise_board(board, board.goals))

# print("---")
# print("SOLUTION:")

solution = solve(board)

board = Board(board_data, goal_data)

if(solution == []):
	print("-1")
else:
	for move in solution:
		print(move)
