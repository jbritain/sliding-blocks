from structures import *
import time

def get_occupied_spaces(board: Board) -> list[list[str]]:
    occupied = [] # what blocks occupy what spaces
    for i in range(board.width): # set all spaces to empty, an empty space has -1
        occupied.append([-1] * board.length)

    for i, block in enumerate(board.blocks):

        for y in range(block.height):
            for x in range(block.width):
                occupied[block.position[0] + x][block.position[1] + y] = i # store the index of the block occupying the space
    return occupied

# finds the moves for a block recursively, moving one space in each direction for each call
# tried_spaces ensures we don't get stuck in a loop by storing spaces we've already tried
# block position is the new position of the block we check around, if no position is provided we use the existing position
# occupied is the result of get_occupied_spaces() for the board
def get_available_moves(block: Block, occupied: list[list[int]], block_position: tuple[int, int] = None, tried_spaces: list[tuple[int, int]] = [], depth = 0) -> list[Move]:
    if block_position is None:
        block_position = block.position
    
    print(f"depth: {depth}")

    moves = []

    if block_position in tried_spaces:
        return moves
    
    tried_spaces.append(block_position)

    if (block_position[0] > 0): # ensure we aren't at the left of the board
        # check the left
        left_occupied = False
        print(f"Checking left position {block_position[1]-1}, {block_position[0]}: ", end="")
        for i in range(block.height): # check all spaces one to the left of the block
            if occupied[block_position[1] + i][block_position[0] - 1] == -1: # space is not empty
                left_occupied = True
                print("occupied")
                break

        if not left_occupied:
            print("unoccupied")
            moves.append(Move(block.position,(block_position[0]-1, block_position[1])))
            moves.extend( get_available_moves(block, occupied, (block_position[0]-1, block_position[1]), tried_spaces, depth=depth+1))

    if (block_position[1] > 0): # ensure we aren't at the top of the board
        # check the top
        top_occupied = False
        print(f"Checking top position {block_position[1]}, {block_position[0]-1}: ", end="")
        for i in range(block.width): # check all spaces one to the top of the block
            if occupied[block_position[1] - 1][block_position[0] + i] == -1: # space is not empty
                top_occupied = True
                print("occupied")
                break
        
        if not top_occupied:
            print("unoccupied")
            moves.append(Move(block.position, (block_position[0], block_position[1]-1)))
            moves.extend( get_available_moves(block, occupied, (block_position[0], block_position[1]-1), tried_spaces, depth=depth+1))

    if (block_position[0] + block.width < len(occupied[0]) - 1): # ensure we aren't at the right of the board
        # check the right
        right_occupied = False
        print(f"Checking right position {block_position[1]+1}, {block_position[0]}: ", end="")
        for i in range(block.height): # check all spaces one to the right of the block
            if occupied[block_position[1] + i][block_position[0] + block.width + 1] == -1: # space is not empty
                right_occupied = True
                print("occupied")
                break
        
        if not right_occupied:
            print("unoccupied")
            moves.append(Move(block.position, (block_position[0]+1, block_position[1])))
            moves.extend( get_available_moves(block, occupied, (block_position[0]+1, block_position[1]), tried_spaces, depth=depth+1))

    if (block_position[1] + block.height < len(occupied) - 1): # ensure we aren't at the bottom of the board
        # check the bottom
        bottom_occupied = False
        print(f"Checking bottom position {block_position[1]}, {block_position[0]+1}: ", end="")
        for i in range(block.width): # check all spaces one to the bottom of the block
            if occupied[block_position[1] + block.height + 1][block_position[0] + i] == -1: # space is not empty
                bottom_occupied = True
                print("occupied")
                break
        
        if not bottom_occupied:
            print("unoccupied")
            moves.append(Move(block.position, (block_position[0], block_position[1]+1)))
            moves.extend( get_available_moves(block, occupied, (block_position[0], block_position[1]+1), tried_spaces, depth=depth+1))

    return moves


# gets all possible moves for a board
def get_all_possible_moves(board: Board) -> list[Move]:
    occupied = get_occupied_spaces(board)

    moves = []

    for i, block in enumerate(board.blocks):
        moves.extend( get_available_moves(block, occupied))

    return moves

    


def solve(board: Board) -> list[Move]:
    if (board.is_solved): # if board is already solved, just move a block to its current position
        return Move(board.blocks[0].position, board.blocks[0].position) 

    start_time = time.time()
    while True:
        if (time.time - start_time) >= 59: # we cannot spend any more time on this puzzle
            return [-1]
    
