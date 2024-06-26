
from structures import Move, vec2, Block, Stack, all_ones
import time
import math

def sign(x):
    return x / abs(x)

def solve(board, debug=False):

    Block.col_sums = {}
    Block.row_sums = {}

    if debug:
        print("Goal:")
        board.visualise(True)
        print("Board:")
        board.visualise()
        
    if board.is_solved():
        return [Move(board.blocks[0].position, vec2(0, 0))] # 'null move'
    global searched_board_states
    searched_board_states = set()
    solution = search_board(board)
    return solution

def explore_board(board, start_time, reverse_move_order=False):
    global searched_board_states
    global iter_count
    moves_and_scores = []

    check_blocks = []

    if board.big_tray:
        gap = board.find_gap()

        directions = sign(board.big_tray_gap - gap) # directions we need to move in

        for block in board.blocks:
            check_col = block.position.x == gap.x or block.position.x == gap.x + directions.x

            check_row = block.position.y == gap.y or block.position.y == gap.y + directions.y

            if check_col and check_row:
                check_blocks.append(block)
    else:
        check_blocks = board.blocks

    for block in check_blocks:
        if time.time() - start_time > 59:
            return []
        moves = block.get_available_moves(board)
        for move in moves:
                board.make_move(move, False)
                board_hash = hash(board)
                if not board_hash in searched_board_states:
                    searched_board_states.add(hash(board))
                    moves_and_scores.append((move, board.rank))
                board.undo_move(move, False)

    moves_and_scores.sort(key = lambda x: x[1], reverse=reverse_move_order)
    return list(map(lambda x: x[0], moves_and_scores))
    

def search_board(board):

    start_time = time.time()

    move_stack = Stack() # stack containing tuples of moves and the depth they must be made at
    
    # initialise stack with available moves from initial board state
    moves_and_depths =  map(lambda x: (x, 0), explore_board(board, start_time, True))
    move_stack.extend(moves_and_depths)

    depth = 0
    while len(move_stack) > 0:


        if board.is_solved():
            return board.moves_made

        if time.time() - start_time > 59:
            return []

        move, move_depth = move_stack.pop() # pop next move from the stack

        depth_difference = depth - move_depth # how many times do we need to undo before we make this move? If the move is at depth 1 and we're at 2 we need to undo once

        for _ in range(depth_difference): # go back up to the depth required to make this move
            depth -= 1
            board.undo_last()
            
        board.make_move(move, True, True)
        depth += 1

        moves_and_depths =  map(lambda x: (x, depth), explore_board(board, start_time, True))
        move_stack.extend(moves_and_depths)

    if board.is_solved():
        return board.moves_made
    return []