import sys
import os
import csv
import cProfile
import time

from structures import *
from solve_checker import *
from solver import *

board_path = None
goal_path = None

try:
	# board_path = "puzzles/hard/big.tray.4"
	# goal_path = "puzzles/hard/many.blocks.20.goal"
	board_path = sys.argv[1]
	goal_path = sys.argv[2]
except Exception:
	pass

#if os.name == 'nt': os.system('cls')


def run_tests():

	easy_puzzles = []
	medium_puzzles = []
	hard_puzzles = []

	with open("puzzles/easy_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "easy/" + row[0].lstrip("(").replace('"', '')
			goal_file = "easy/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			easy_puzzles.append((puzzle_file, goal_file, possible))
	
	with open("puzzles/medium_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "medium/" + row[0].lstrip("(").replace('"', '')
			goal_file = "medium/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			medium_puzzles.append((puzzle_file, goal_file, possible))
	
	with open("puzzles/hard_puzzles.csv") as easy_file:
		puzzle_reader = csv.reader(easy_file)
		for row in puzzle_reader:
			puzzle_file = "hard/" + row[0].lstrip("(").replace('"', '')
			goal_file = "hard/" + row[1].lstrip(" ").replace('"', '')
			possible = row[2] == "False)"

			hard_puzzles.append((puzzle_file, goal_file, possible))

	successful = 0
	failed = 0
	easy_marks = 40
	medium_marks = 0
	hard_marks = 0


	for puzzle in easy_puzzles + medium_puzzles + hard_puzzles:
		board_path = f"./puzzles/{puzzle[0]}"
		goal_path = f"./puzzles/{puzzle[1]}"
		possible = puzzle[2]

		print(puzzle[0], end=' ')

		
		with open(board_path) as bf:
			board_data = bf.read()

		with open(goal_path) as gf:
			goal_data = gf.read()

		board = board_from_string(board_data, goal_data)
		board_copy = copy.deepcopy(board)

		try:
			start_time = time.time()
			solution = solve(board, False)
			exec_time = time.time() - start_time
			if exec_time > 60:
				print("FAIL - OVERTIME", end="")
				failed += 1
				if puzzle in easy_puzzles:
					easy_marks = 0
			elif solution != []:
				solution_correct = try_solution(board_copy, solution, False)
				if(solution_correct == possible):
					print("PASS", end="")
					successful += 1
					if puzzle in medium_puzzles:
						medium_marks += 0.5
					elif puzzle in hard_puzzles:
						hard_marks += 1.5
				else:
					print("INCORRECT SOLUTION - FAIL", end="")
					failed += 1
					if puzzle in easy_puzzles:
						easy_marks = 0
			else:
				if possible:
					print("FAIL", end="")
					failed += 1
					if puzzle in easy_puzzles:
						easy_marks = 0
				else:
					print("PASS", end="")
					successful += 1
					if puzzle in medium_puzzles:
						medium_marks += 0.5
					elif puzzle in hard_puzzles:
						hard_marks += 1.5
		except RecursionError:
			sys.stdout.close()
			print("FAIL (recursion depth exceeded)", end="")
			failed += 1
		
		print(' (impossible)' if not possible else '')

		
	print(f"{successful} tests of {successful + failed} passed [{(successful * 100) / (successful + failed)}]%")
	print(f"You will get {easy_marks + max(medium_marks, 19) + max(hard_marks, 41)} marks")

# if board_path == goal_path == None:
# 	#cProfile.run("run_tests()", sort="tottime")
# 	if os.name == 'nt': os.system('cls')
# 	run_tests()
# else:
with open(board_path) as bf:
	#sys.stdout = open(f"./output.txt", "w+", encoding="utf-8")
	
	board_data = bf.read()

	with open(goal_path) as gf:
		goal_data = gf.read()

	board = board_from_string(board_data, goal_data)
	board_copy = copy.deepcopy(board)
	solution = solve(board, False)

	if(solution == []):
		print("-1")
	else:
		for move in solution:
			print(move)

	#print(try_solution(board_copy, solution, True))

#sys.stdout.close()