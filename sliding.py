import sys
import os
import csv

from structures import *
from solve_checker import *
from solver import *

board_path = None
goal_path = None

try:
	# board_path = "puzzles/medium/c15"
	# goal_path = "puzzles/medium/15.23-27.30.41.goal"
	board_path = sys.argv[1] 
	goal_path = sys.argv[2]
except Exception:
	pass

if os.name == 'nt': os.system('cls')


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

		board = board_from_string(board_data, goal_data)

		try:
			solution = solve(board)

			if solution != -1:
				solution_correct = try_solution(board, solution, False)
				if(solution_correct == possible):
					print("PASS", end="")
					successful += 1
				else:
					print("FAIL (incorrect solution)", end="")
					failed += 1
			else:
				if possible:
					print("FAIL (no solution or timeout)", end="")
					failed += 1
				else:
					print("PASS", end="")
					successful += 1
		except RecursionError:
			sys.stdout.close()
			print("FAIL (recursion depth exceeded)", end="")
			failed += 1
		
		print(' (impossible)' if not possible else '')
		
	print(f"{successful} tests of {successful + failed} passed [{(successful * 100) / (successful + failed)}]%")

if board_path == goal_path == None:
	run_tests()
else:
	with open(board_path) as bf:
		#sys.stdout = open(f"./output.txt", "w+", encoding="utf-8")
		if not 'easy' in board_path:
			print("-1")
			sys.exit()

		board_data = bf.read()

		with open(goal_path) as gf:
			goal_data = gf.read()

		board = board_from_string(board_data, goal_data)
		solution = solve(board, False)
		if(solution == []):
			print("-1")
		else:
			for move in solution:
				print(move)

		#print(try_solution(board, solution))

sys.stdout.close()