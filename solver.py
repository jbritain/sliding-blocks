import copy
from structures import Move, vec2, Block
import time

recurse_limit = 900

def solve(board, debug=False):

    Block.col_sums = {}
    Block.row_sums = {}

    if debug:
        print("Goal:")
        board.visualise(True)
    if board.is_solved():
        return [Move(board.blocks[0].position, vec2(0, 0))] # 'null move'
    global searched_board_states
    searched_board_states = set()
    solution = search_board(board, debug, time.time())
    return solution

def search_board(board, debug, start_time, depth=0):   
    if time.time() - start_time >= 59: # out of time, I hope this puzzle is impossible
        return []
        


    if debug: print(f"----->{depth}")
    if board.is_solved(): # we did it chat
        return True
    
    if depth == recurse_limit:
        if debug: 
            print("Excessive depth reached")
            print(f"{depth - 1}<---------")
            # pass
        return []

    global searched_board_states
    if debug:
        print("Searching board...")
        board.visualise()

    searched_board_states.add(hash(board))
    if hash(board) == -8471149908106808705:
        pass

    moves_and_scores = [] # tuples - first item is the move, second is the resultant board
    for block in board.blocks:
        if debug: print(f"Checking block at position {block.position}")
        moves = block.get_available_moves(board)
        
        for move in moves:
            if debug: print(f"    Found move {move}", end="")
            board.make_move(move, False)
            board_hash = hash(board)
            if debug: print(f" {board_hash}", end="")
            if not board_hash in searched_board_states:
                if debug: print(f" with score {board.rank}")
                moves_and_scores.append((move, board.rank))
            else:
                if debug: print(f" (duplicate board)")
                pass
            board.undo_move(move, False)

    moves_and_scores.sort(key = lambda x: x[1]) # sort by ranking of resultant board

    for move, _ in moves_and_scores:
        if debug: print(f"Trying move {move} at depth {depth}")
        board.make_move(move)
        result = search_board(board, debug, start_time, depth+1)
        board.undo_move(move)
        if result != []: # if we get anything other than an empty list back
            if result is True: # this board is solved so the move is the final one
                return [move] # return only that

            return [move] + result # otherwise return the move it returned and our move

    if debug: print(f"{depth - 1}<---------")
    if depth == 0:
        if time.time() - start_time >= 59: # out of time, I hope this puzzle is impossible
            print("TIMEOUT - ", end="")
        else:
            print("NO SOLUTION - ", end="")
    return [] # bad luck, dead end
