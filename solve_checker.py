from structures import *
from visual import visualise_board
import copy

def try_solution(board: Board, moves: list[Move]) -> bool:
    test_board = copy.deepcopy(board)

    for move in moves:
        print(visualise_board(test_board))
        test_board.make_move(move)
        print(move)
    print(visualise_board(test_board))
    
    if(test_board.is_solved()):
        print("Solution is correct")
    else:
        print("Solution is incorrect")

