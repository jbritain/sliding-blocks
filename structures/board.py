from .vec import vec2
from .block import Block

class Board:
    # blocks and goals are lists of blocks
    def __init__(self, width, length, blocks, goals):
        self.size = vec2(width, length)
        self.blocks = blocks
        self.goals = goals


def board_from_string(board_string, goal_string):
    # set up the board
    board_lines = [l for l in board_string.split("\n") if l]
    dims = board_lines[0].split(" ")
    length = dims[0]
    width = dims[1]

    blocks = []
    
    for line in board_lines[1:]:
        data = line.split(" ")
        blocks.append(Block(int(data[2]), int(data[3]), int(data[1]), int(data[0])))

    goal_lines = goal_string.split("\n")

    goals = []
    for line in goal_lines:
        if line:
            data = line.split(" ")
            goals.append(Block(int(data[2]), int(data[3]), int(data[1]), int(data[0])))

    return Board(width, length, blocks, goals)