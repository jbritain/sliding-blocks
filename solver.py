import copy
from structures import Move
import time

def solve(board, debug=False):
    if debug:
        print("Goal:")
        board.visualise(True)
    if board.is_solved():
        return [Move(board.blocks[0].position, board.blocks[0].position)] # 'null move'
    global searched_board_states
    searched_board_states = set()
    solution = search_board(board, debug, time.time())
    return solution

def search_board(board, debug, start_time, depth=0):
    if not debug and time.time() - start_time >= 59: # out of time, I hope this puzzle is impossible
        return []
    if depth >= 100:
        if debug: 
            print("Excessive depth reached")
            print(f"{depth - 1}<---------")
        return []

    if debug: print(f"----->{depth}")
    if board.is_solved(): # we did it chat
        return True

    global searched_board_states
    searched_board_states.add(board)
    if debug:
        print("Searching board...")
        board.visualise()

    moves_and_boards = [] # tuples - first item is the move, second is the resultant board
    for block in board.blocks:
        if debug: print(f"Checking block at position {block.position}")
        moves = block.get_available_moves(board)
        
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.make_move(move)
            if not new_board in searched_board_states:
                moves_and_boards.append((move, new_board))
            else:
                if debug: print(f"Move {move} results in duplicate board")

    moves_and_boards.sort(key = lambda x: x[1].rank) # sort by ranking of resultant board
    if debug: print(f"Found {len(moves_and_boards)} moves:")
    for move, board in moves_and_boards:
        if debug: print(f"    {move} with score {board.rank}")

    for move, new_board in moves_and_boards:
        if debug: print(f"Trying move {move} at depth {depth}")
        result = search_board(new_board, debug, start_time, depth+1)
        if result != []: # if we get anything other than an empty list back
            if result is True: # this board is solved so the move is the final one
                return [move] # return only that

            return [move] + result # otherwise return the move it returned and our move

    if debug: print(f"{depth - 1}<---------")
    return [] # bad luck, dead end
