
from structures import Move, vec2, Block, Stack
import sys

recurse_limit = 1700
sys.setrecursionlimit(recurse_limit + 50)

def solve(board, debug=False):

    Block.col_sums = {}
    Block.row_sums = {}

    if debug:
        if debug: print("Goal:")
        board.visualise(True)
    if board.is_solved():
        return [Move(board.blocks[0].position, vec2(0, 0))] # 'null move'
    global searched_board_states
    searched_board_states = set()
    solution = search_board_non_recursive(board, debug)
    return solution

def explore_board(board, reverse_move_order=False, debug=False):
    global searched_board_states
    moves_and_scores = []
    for block in board.blocks:
        moves = block.get_available_moves(board)
        for move in moves:
                if debug: print(f"    Found move {move}", end="")
                board.make_move(move, False)
                board_hash = hash(board)
                if debug: print(f" {board_hash}", end="")
                if not board_hash in searched_board_states:
                    searched_board_states.add(hash(board))
                    if debug: print(f" with score {board.rank}")
                    moves_and_scores.append((move, board.rank))
                else:
                    if debug: print(f" (duplicate board)")
                    pass
                board.undo_move(move, False)

    moves_and_scores.sort(key = lambda x: x[1], reverse=reverse_move_order)
    return list(map(lambda x: x[0], moves_and_scores))
    

def search_board_non_recursive(board, debug):
    move_stack = Stack() # stack containing tuples of moves and the depth they must be made at

    # initialise stack with available moves from initial board state
    moves_and_depths =  map(lambda x: (x, 0), explore_board(board, True, debug))
    move_stack.extend(moves_and_depths)

    depth = 0
    while len(move_stack) > 0:

        if board.is_solved():
            if debug: print("Solved!")
            return board.moves_made

        move, move_depth = move_stack.pop() # pop next move from the stack

        depth_difference = depth - move_depth # how many times do we need to undo before we make this move? If the move is at depth 1 and we're at 2 we need to undo once

        for _ in range(depth_difference): # go back up to the depth required to make this move
            depth -= 1
            if debug: print(f"{depth}<---------")
            board.undo_last()
            
        if debug: board.visualise()
        if debug: print(f"trying move {move} at depth {depth}")
        board.make_move(move, True, True)
        depth += 1

        moves_and_depths =  map(lambda x: (x, depth), explore_board(board, True, debug))
        move_stack.extend(moves_and_depths)

    if board.is_solved():
        if debug: print("Solved!")
        return board.moves_made
    return []



def search_board(board, debug, start_time, depth=0):   
    if time.time() - start_time >= 59: # out of time, I hope this puzzle is impossible
        return []
        


    #if debug: if debug: print(f"----->{depth}")
    if board.is_solved(): # we did it chat
        return True
    
    if depth == recurse_limit:
        #if debug: 
            # if debug: print("Excessive depth reached")
            # if debug: print(f"{depth - 1}<---------")
            # # pass
        return []

    global searched_board_states
    #if debug:
        # if debug: print("Searching board...")
        # #board.visusalise()

    searched_board_states.add(hash(board))

    moves_and_scores = [] # tuples - first item is the move, second is the resultant board
    for block in board.blocks:
        #if debug: if debug: print(f"Checking block at position {block.position}")
        moves = block.get_available_moves(board)
        
        for move in moves:
            #if debug: if debug: print(f"    Found move {move}", end="")
            board.make_move(move, False)
            board_hash = hash(board)
            #if debug: if debug: print(f" {board_hash}", end="")
            if not board_hash in searched_board_states:
                #if debug: if debug: print(f" with score {board.rank}")
                moves_and_scores.append((move, board.rank))
            else:
                #if debug: if debug: print(f" (duplicate board)")
                pass
            board.undo_move(move, False)

    moves_and_scores.sort(key = lambda x: x[1]) # sort by ranking of resultant board

    for move, _ in moves_and_scores:
        #if debug: if debug: print(f"Trying move {move} at depth {depth}")
        board.make_move(move)
        result = search_board(board, debug, start_time, depth+1)
        board.undo_move(move)
        if result != []: # if we get anything other than an empty list back
            if result is True: # this board is solved so the move is the final one
                return [move] # return only that

            return [move] + result # otherwise return the move it returned and our move

    #if debug: if debug: print(f"{depth - 1}<---------")
    # if depth == 0:
    #     if time.time() - start_time >= 59: # out of time, I hope this puzzle is impossible
    #         if debug: print("TIMEOUT - ", end="")
    #     else:
    #         if debug: print("NO SOLUTION - ", end="")
    return [] # bad luck, dead end