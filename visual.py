from structures import *

def get_char(block_id: int):
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
    ]

    return chars[block_id % (len(chars) - 1)]

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

    if not blocks:
        blocks = board.blocks

    print(f"{board.width}x{board.length}")
    vis = []
    for i in range(board.length - 1):
        vis.append(["  "] * (board.width))

    for i, block in enumerate(blocks):
        char = get_char(i) + " "

        for y in range(block.height):
            for x in range(block.width):
                vis[block.position[1] + y][block.position[0] + x] = char

    rows = []
    rows.append("┌" + "─" * ((board.width) * 2) + "┐")
    for row in vis:
        row += ["│"]
        row = ["│"] + row
        rows.append(''.join(row))
    rows.append("└" + "─" * ((board.width) * 2) + "┘")
    return '\n'.join(rows)