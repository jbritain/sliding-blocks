from structures import *
from visual import visualise_board
import copy

def try_solution(board: Board, moves: list[Move]) -> bool:
    test_board = copy.deepcopy(board)

    for move in moves:
        print(visualise_board(test_board))
        print("---")
        test_board.make_move(move)
    print(visualise_board(test_board))
    
    print(board.is_solved())

