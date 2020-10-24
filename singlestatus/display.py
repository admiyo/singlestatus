from singlestatus import common


CROSS_BARS = ["┼", "┿", "╂", "╋"]


def is_bold(val):
    return val % common.BASIS == 0


def draw_tee(tee, dim):
    piece = ord(tee[0]) + 3
    if is_bold(dim):
        piece = piece + 4
    print("%c" % piece, end='')


def draw_cross(row, col):
    piece = 0
    if is_bold(row):
        piece = piece + 1
    if is_bold(col):
        piece = piece + 2
    print("%c" % CROSS_BARS[piece], end='')


def draw_padding():
    print("         ", end='')


def pad_row():
    for col in range(common.DIM):
        if col % common.BASIS != 0:
            print("│", end="")
        else:
            print("┃", end="")
        draw_padding()
    print("┃")


def draw_cell_length(bold=False):
    for _ in range(9):
        if bold:
            print("━", end='')
        else:
            print("─", end='')


def draw_board(board):
    print("┏", end="")
    for col in range(common.DIM):
        if col > 0:
            draw_tee('┬', col)
        draw_cell_length(True)
    print("┓")

    for row in range(common.DIM):
        if (row > 0):
            if is_bold(row):
                print("┣", end='')
            else:
                print("┠", end='')

            for col in range(common.DIM):
                if col > 0:
                    draw_cross(row, col)
                draw_cell_length(is_bold(row))
            if is_bold(row):
                print("┫", end='')
            else:
                print("┨", end='')
            print("")
        pad_row()
        for col in range(common.DIM):
            if col % common.BASIS != 0:
                print("│", end="")
            else:
                print("┃", end="")
            print(board[row][col].strip().center(9, ' '), end="")
        print("┃")
        pad_row()

    print("┗", end='')
    for col in range(common.DIM):
        if col > 0:
            draw_tee('┴', col)
        draw_cell_length(True)
    print("┛")


def draw_puzzle(puzzle):
    puzzle_array = common.puzzle_to_array(puzzle)

    for row in range(common.DIM):
        for col in range(common.DIM):
            if col == 0:
                print()

            c = ord(puzzle_array[row][col]) - ord('0')
            if c == 0:
                print("  ", end="")
            else:
                print(" %d" % c, end="")
    print()
