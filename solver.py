from structures import *
from visual import *
import time
import copy

# finds the moves for a block recursively, moving one space in each direction for each call
# tried_spaces ensures we don't get stuck in a loop by storing spaces we've already tried
# block position is the new position of the block we check around, if no position is provided we use the existing position
# occupied is the result of get_occupied_spaces() for the board




def search_board(board: Board, start_time: float, depth: int = 0) -> list[Move]:
    print("---")
    print(f"Depth: {depth}")
    print("Searching board...")
    print(visualise_board(board))

    if(time.time() - start_time > 59):
        return []

    global tried_board_states
    print(f"New tried board ID: {len(tried_board_states)}")
    tried_board_states.append(board)

    moves = board.get_all_possible_moves()
    
    moves_and_boards = [] # list of moves and their resultant boards (i.e the board and the move that got it there)
    for next_move in moves:
        next_board = copy.deepcopy(board)
        next_board.make_move(next_move)

        if next_board.is_solved(): # check if any of them are solved, in which case this is the move we want
            print(f"Trying move {next_move}")
            print(f"Depth: {depth+1}")
            print("Searching board...")
            print(visualise_board(board))
            print("Solution found!")
            return [next_move]
        
        if not next_board in tried_board_states: # check if we have already tried any of them
            moves_and_boards.append((next_move, next_board))
            
        else:
            print(f"Move {next_move} results in repeat board ID: {tried_board_states.index(next_board)}")
    
    print(f"Found {len(moves_and_boards)} possible moves")


    moves_and_boards.sort(key=lambda b: b[1].rank(), reverse=False) # rank moves by how good their boards are
    for move_and_board in moves_and_boards:
        print(f"Move {move_and_board[0]} has score {move_and_board[1].rank()}")

    for i, next_move_and_board in enumerate(moves_and_boards):
        print("---")
        print(visualise_board(board))
        print(f"Trying move {next_move_and_board[0]} ({i + 1} of {len(moves_and_boards)})")
        print(f"->{depth + 1}")
        res = search_board(next_move_and_board[1], start_time, depth + 1)
        if res != []:
            print(f"move {next_move} success")
            return [next_move_and_board[0]] + res

    print(f"{depth - 1}<-")
    return []


def solve(board: Board) -> list[Move]:
    global tried_board_states
    tried_board_states = []
    
    print("Goal")
    print(visualise_board(board, board.goals))

    print("Solve")

    if (board.is_solved()): # if board is already solved, just move a block to its current position
        return [Move(board.blocks[0].position, board.blocks[0].position)]

    start_time = time.time()

    solution = search_board(copy.deepcopy(board), start_time)

    if solution == []:
        return -1

    return solution


    
