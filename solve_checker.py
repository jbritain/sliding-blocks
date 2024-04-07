import copy

def try_solution(board, solution, debug=True):
    
    test_board = copy.deepcopy(board)
    if debug:
        print("GOAL")
        test_board.visualise(True)
        print("SOLUTION")
        test_board.visualise()
    for move in solution:
        test_board.make_move(move)
        if debug:
            print(move)
            test_board.visualise()
            print("---")
    if(test_board.is_solved()):
        return True
    return False