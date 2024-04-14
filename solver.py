
from structures import Move, vec2, Block, Stack

iter_limit = 1000000

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
    solution = search_board(board, debug)
    return solution

def explore_board(board, reverse_move_order=False, debug=False):
    global searched_board_states
    global iter_count
    moves_and_scores = []
    for block in board.blocks:
        iter_count += 1
        if iter_count > iter_limit:
            return []
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
    

def search_board(board, debug):

    global iter_count
    iter_count = 0
    move_stack = Stack() # stack containing tuples of moves and the depth they must be made at
    
    # initialise stack with available moves from initial board state
    moves_and_depths =  map(lambda x: (x, 0), explore_board(board, True, debug))
    move_stack.extend(moves_and_depths)

    depth = 0
    while len(move_stack) > 0:


        if board.is_solved():
            if debug: print("Solved!")
            return board.moves_made

        if iter_count > iter_limit:
            return []

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