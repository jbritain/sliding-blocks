from structures import *

def visualise_board(board: Board) -> str:
    chars = [
        "X",
        "#",
        "H",
        "%",
        "&",
        "@",
        "$",
        "*",
        "K",
        "O"
    ]

    vis = []
    for i in range(board.width):
        vis.append([" "] * board.length)

    for i, block in enumerate(board.blocks):
        char = chars[i % (len(chars) - 1)]

        for y in range(block.height):
            for x in range(block.width):
                vis[block.position[0] + x][block.position[1] + y] = char

    rows = []
    for row in vis:
        rows.append(''.join(row))
    return '\n'.join(rows)
