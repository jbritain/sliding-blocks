from structures import *
from visual import *
import time
import copy

def get_occupied_spaces(board: Board) -> list[list[str]]:
    occupied = [] # what blocks occupy what spaces
    for i in range(board.width): # set all spaces to empty, an empty space has -1
        occupied.append([-1] * board.length)

    for i, block in enumerate(board.blocks):

        for y in range(block.height):
            for x in range(block.width):
                occupied[block.position[1] + y][block.position[0] + x] = i # store the index of the block occupying the space
    return occupied

# finds the moves for a block recursively, moving one space in each direction for each call
# tried_spaces ensures we don't get stuck in a loop by storing spaces we've already tried
# block position is the new position of the block we check around, if no position is provided we use the existing position
# occupied is the result of get_occupied_spaces() for the board
def get_available_moves(block_id: int, board: Board) -> list[Move]:

    block = board.blocks[block_id]
    block_position = block.position

    occupied = get_occupied_spaces(board)

    moves = []

    if (block_position[0] > 0): # ensure we aren't at the left of the board
        # check the left
        left_occupied = False
        #print(f"Checking left position {block_position[0]-1}, {block_position[1]}: ", end="")
        for i in range(block.height): # check all spaces one to the left of the block
            if occupied[block_position[1] + i][block_position[0] - 1] != -1: # space is not empty
                left_occupied = True
                #print("occupied")
                break

        if not left_occupied:
            #print("unoccupied")
            move = Move(block.position,(block_position[0]-1, block_position[1]))
            moves.append(move)

    if (block_position[1] > 0): # ensure we aren't at the top of the board
        # check the top
        top_occupied = False
        #print(f"Checking top position {block_position[0]}, {block_position[1]-1}: ", end="")
        for i in range(block.width): # check all spaces one to the top of the block
            if occupied[block_position[1] - 1][block_position[0] + i] != -1: # space is not empty
                top_occupied = True
                #print("occupied")
                break
        
        if not top_occupied:
            #print("unoccupied")
            move = Move(block.position, (block_position[0], block_position[1]-1))
            moves.append(move)

    if (block_position[0] + block.width < len(occupied[0]) - 1): # ensure we aren't at the right of the board
        # check the right
        right_occupied = False
        #print(f"Checking right position {block_position[0]+1}, {block_position[1]}: ", end="")
        for i in range(block.height): # check all spaces one to the right of the block
            if occupied[block_position[1] + i][block_position[0] + block.width] != -1: # space is not empty
                right_occupied = True
                #print("occupied")
                break
        
        if not right_occupied:
            #print("unoccupied")
            move = Move(block.position, (block_position[0]+1, block_position[1]))
            moves.append(move)

    if (block_position[1] + block.height < len(occupied) - 1): # ensure we aren't at the bottom of the board
        # check the bottom
        bottom_occupied = False
        #print(f"Checking bottom position {block_position[0]}, {block_position[1]+1}: ", end="")
        for i in range(block.width): # check all spaces one to the bottom of the block
            if occupied[block_position[1] + block.height][block_position[0] + i] != -1: # space is not empty
                bottom_occupied = True
                #print("occupied")
                break
        
        if not bottom_occupied:
            #print("unoccupied")
            move = Move(block.position, (block_position[0], block_position[1]+1))
            moves.append(move)

    return moves


# gets all possible moves for a board
def get_all_possible_moves(board: Board) -> list[Move]:

    moves = []

    for block_id, block in enumerate(board.blocks):
        moves.extend(get_available_moves(block_id, board))

    return moves

def search_move(board: Board, start_time: float, move: Move = None, depth: int = 0) -> list[Move]:
    move_queue = Queue()

    tried_board_states = []
    
    inital_moves = get_all_possible_moves(board)
    for move in inital_moves:
        move_queue.enqueue((board, move, []))

    while len(move_queue) > 0:
        if time.time() - start_time > 59:
            return -1

        (board, move, previous_moves) = move_queue.dequeue()

        test_board = copy.deepcopy(board)
        test_board.make_move(move)

        if(test_board in tried_board_states):
            continue # we already tried this board

        tried_board_states.append(test_board)

        if(test_board.is_solved()):
            return previous_moves + [move] # we did it chat
        else:
            new_moves = get_all_possible_moves(test_board)
            for next_move in new_moves:
                move_queue.enqueue((test_board, next_move, previous_moves + [move]))

    return -1



    
    
    return []


def solve(board: Board) -> list[Move]:
    if (board.is_solved()): # if board is already solved, just move a block to its current position
        return [Move(board.blocks[0].position, board.blocks[0].position)]

    start_time = time.time()

    solution = search_move(copy.deepcopy(board), start_time)

    if solution == []:
        return -1

    return solution


    
