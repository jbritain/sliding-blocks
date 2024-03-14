from structures import *
import copy

def try_solution(board: Board, moves: list[Move]) -> bool:
    test_board = copy.deepcopy(board)

    for move in moves:
        test_board.make_move(move)

    print(board.is_solved())

