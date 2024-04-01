from structures import *
from visual import *
import time
import copy

def get_occupied_spaces(board: Board) -> list[list[bool]]:
    occupied = [] # what blocks occupy what spaces
    for _ in range(board.width): # set all spaces to empty, an empty space has -1
        occupied.append([False] * board.length)

    for block in board.blocks:
        for y in range(block.height):
            for x in range(block.width):
                occupied[block.position[1] + y][block.position[0] + x] = True # store the id of the block occupying the space
    return occupied

# finds the moves for a block recursively, moving one space in each direction for each call
# tried_spaces ensures we don't get stuck in a loop by storing spaces we've already tried
# block position is the new position of the block we check around, if no position is provided we use the existing position
# occupied is the result of get_occupied_spaces() for the board
def get_available_moves(block: Block, board: Board) -> list[Move]:

    block_position = block.position

    occupied = get_occupied_spaces(board)

    moves = []

    #print(f"Checking block at {block.position}")

    if (block_position[0] > 0): # ensure we aren't at the left of the board
        # check the left
        left_occupied = False
        #print(f"Checking left position {block_position[0]-1}, {block_position[1]}: ", end="")
        for i in range(block.height): # check all spaces one to the left of the block
            if occupied[block_position[1] + i][block_position[0] - 1]: # space is not empty
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
            if occupied[block_position[1] - 1][block_position[0] + i]: # space is not empty
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
            if occupied[block_position[1] + i][block_position[0] + block.width]: # space is not empty
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
            if occupied[block_position[1] + block.height][block_position[0] + i]: # space is not empty
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

    for block in board.blocks:
        moves.extend(get_available_moves(block, board))

    return moves


def search_board(board: Board, start_time: float, depth: int = 0) -> list[Move]:
    #print(f"Depth: {depth}")
    #print("Searching board...")
    #print(visualise_board(board))

    global tried_board_states
    tried_board_states.add(board)

    moves = get_all_possible_moves(board)
    
    moves_and_boards = [] # list of moves and their resultant boards (i.e the board and the move that got it there)
    for next_move in moves:
        next_board = copy.deepcopy(board)
        next_board.make_move(next_move)

        if next_board.is_solved(): # check if any of them are solved, in which case this is the move we want
            #print(f"Trying move {next_move}")
            #print(f"Depth: {depth+1}")
            #print("Searching board...")
            #print(visualise_board(board))
            #print("Solution found!")
            return [next_move]
        
        if not next_board in tried_board_states: # check if we have already tried any of them
            moves_and_boards.append((next_move, next_board))
    
    #print(f"Found {len(moves_and_boards)} possible moves")


    moves_and_boards.sort(key=lambda b: b[1].rank(), reverse=False) # rank moves by how good their boards are

    for next_move_and_board in moves_and_boards:
        #print(f"Trying move {next_move_and_board[0]}")
        res = search_board(next_move_and_board[1], start_time, depth + 1)
        if res != []:
            #print(f"move {next_move} success")
            return [next_move_and_board[0]] + res

    return []


def solve(board: Board) -> list[Move]:
    global tried_board_states
    tried_board_states = set()

    if (board.is_solved()): # if board is already solved, just move a block to its current position
        return [Move(board.blocks[0].position, board.blocks[0].position)]

    start_time = time.time()

    solution = search_board(copy.deepcopy(board), start_time)

    if solution == []:
        return -1

    return solution


    
