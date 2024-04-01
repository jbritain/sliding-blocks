from structures import *
from visual import visualise_board
import copy

def try_solution(board: Board, moves: list[Move], debug = True) -> bool:
    test_board = copy.deepcopy(board)

    if debug:
        print("GOAL:")
        print(visualise_board(test_board, test_board.goals))
        print("TEST:")

    for move in moves:
        if debug: print(visualise_board(test_board))
        if debug: print(move)
        test_board.make_move(move)
    if debug: print(visualise_board(test_board))
    
    return test_board.is_solved()

