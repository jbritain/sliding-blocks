import sys
import os

os.system("cls")

from structures import *
from solve_checker import *
from solver import *

board_path = "puzzles/easy/big.block.1"# sys.argv[1]
goal_path = "puzzles/easy/big.block.1.goal" # sys.argv[2]

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
# board = Board(
# 	"5 4\n2 1 0 0\n2 1 0 3\n2 1 2 0\n2 1 2 3\n2 2 1 1\n1 2 3 1\n1 1 4 0\n1 1 4 1\n1 1 4 2\n1 1 4 3",
# 	"2 2 3 1"
# )

solution = solve(board)
if(solution == []):
	print("-1")
else:
	for move in solution:
		print(move)
