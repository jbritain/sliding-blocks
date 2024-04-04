import sys
import os
import csv

from structures import *
from solve_checker import *
from solver import *

board_path = None
goal_path = None

sys.stdout = open("./output.txt", "w", encoding="utf-8")

try:
	board_path = "puzzles/medium/c15" #sys.argv[1] 
	goal_path = "puzzles/medium/15.23-27.30.41.goal"#sys.argv[2]
except Exception:
	pass

os.system("cls")


def run_tests():


	puzzles = []

	with open("puzzles/easy_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "easy/" + row[0].lstrip("(").replace('"', '')
			goal_file = "easy/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			puzzles.append((puzzle_file, goal_file, possible))
	
	with open("puzzles/medium_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "medium/" + row[0].lstrip("(").replace('"', '')
			goal_file = "medium/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			puzzles.append((puzzle_file, goal_file, possible))
	
	with open("puzzles/hard_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "hard/" + row[0].lstrip("(").replace('"', '')
			goal_file = "hard/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			puzzles.append((puzzle_file, goal_file, possible))

	successful = 0
	failed = 0


	for puzzle in puzzles:
		board_path = f"./puzzles/{puzzle[0]}"
		goal_path = f"./puzzles/{puzzle[1]}"
		possible = puzzle[2]

		print(puzzle[0], end=' ')
		
		with open(board_path) as bf:
			board_data = bf.read()

		with open(goal_path) as gf:
			goal_data = gf.read()

		board = Board(board_data, goal_data)

		try:
			solution = solve(board)

			if solution != -1:
				solution_correct = try_solution(board, solution, False)
				if(solution_correct == possible):
					print(f"PASS{' (impossible)' if not possible else ''}")
					successful += 1
				else:
					print("FAIL (incorrect solution)")
					failed += 1
			else:
				if possible:
					print("FAIL (no solution or timeout)")
					failed += 1
				else:
					print("PASS")
					successful += 1
		except RecursionError:
			print("FAIL (recursion depth exceeded)")
			failed += 1
		
	print(f"{successful} tests of {successful + failed} passed [{(successful * 100) / (successful + failed)}]%")

if board_path == goal_path == None or True:
	run_tests()
else:
	with open(board_path) as bf:
		board_data = bf.read()

		with open(goal_path) as gf:
			goal_data = gf.read()

		board = Board(board_data, goal_data)
		solution = solve(board)
		if(solution == -1):
			print("-1")
		else:
			for move in solution:
				print(move)

		print(try_solution(board, solution))

sys.stdout.close()