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
    if (time.time() - start_time) >= 59: # we cannot spend any more time on this puzzle
        return []
    
    #print("---")
    #print(f"Trying move {move}")
    #print(f"depth: {depth}")

    global tried_board_states
    
    search_board = copy.deepcopy(board)
    if move:
        search_board.make_move(move)
        
    #print(visualise_board(search_board))

    for tried_board in tried_board_states:
        if tried_board == search_board:
            #print("Board already tested")
            return []

    if (board.is_solved()):
       #print(visualise_board(board))
        return [Move((-1, -1), (-1, -1))]
    
    tried_board_states.append(search_board)
    
    possible_moves = get_all_possible_moves(search_board)

   ##print(f"found {len(possible_moves)} possible moves")
    
    for next_move in possible_moves:
        tried_move = search_move(search_board, start_time, next_move, depth+1)
        if tried_move != []:
            if move:
                return [move] + tried_move
            else:
                return tried_move
    
    return []


def solve(board: Board) -> list[Move]:
    global tried_board_states # ooer global variables??? this is so that the multiple recursive threads can all avoid checking board states we have already checked
    tried_board_states = []

    if (board.is_solved()): # if board is already solved, just move a block to its current position
        return [Move(board.blocks[0].position, board.blocks[0].position)]

    start_time = time.time()

    solution = search_move(board, start_time)
    solution = solution[:-1] # remove last move since this takes us away from the solution

    if solution == []:
        return -1

    return solution


    
