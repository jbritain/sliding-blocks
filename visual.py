from structures import *

def visualise_board(board: Board, blocks: list[Block] = None) -> str:
    # chars = [
    #     "X",
    #     "#",
    #     "H",
    #     "%",
    #     "&",
    #     "@",
    #     "$",
    #     "*",
    #     "K",
    #     "O"
    # ]
    chars = [
        "■",
        "□",
        "▣",
        "▤",
        "▥",
        "▦",
        "▧",
        "▨",
        "▩",
        "◘",
        "◙"
    ]

    if not blocks:
        blocks = board.blocks

    vis = []
    for i in range(board.length):
        vis.append(["  "] * board.width)

    for i, block in enumerate(blocks):
        char = chars[i % (len(chars) - 1)] + " "

        for y in range(block.height):
            for x in range(block.width):
                vis[block.position[1] + y][block.position[0] + x] = char

    rows = []
    rows.append("┌" + "─" * (board.width * 2) + "┐")
    for row in vis:
        row += ["│"]
        row = ["│"] + row
        rows.append(''.join(row))
    rows.append("└" + "─" * (board.width * 2) + "┘")
    return '\n'.join(rows)