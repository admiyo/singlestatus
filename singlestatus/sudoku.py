#!/bin/python
import math
from singlestatus import samples

BASIS = 3
DIM = BASIS * BASIS
HALFISH = (DIM - 1) / 2
CROSS_BARS = ["┼", "┿", "╂", "╋"]
FULL_SET = "123456789"


def is_bold(val):
    return val % BASIS == 0


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


def draw_set():
    print(FULL_SET, end='')


def draw_padding():
    print("         ", end='')


def pad_row():
    for col in range(DIM):
        if col % BASIS != 0:
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
    for col in range(DIM):
        if col > 0:
            draw_tee('┬', col)
        draw_cell_length(True)
    print("┓")

    for row in range(DIM):
        if (row > 0):
            if is_bold(row):
                print("┣", end='')
            else:
                print("┠", end='')

            for col in range(DIM):
                if col > 0:
                    draw_cross(row, col)
                draw_cell_length(is_bold(row))
            if is_bold(row):
                print("┫", end='')
            else:
                print("┨", end='')
            print("")
        pad_row()
        for col in range(DIM):
            if col % BASIS != 0:
                print("│", end="")
            else:
                print("┃", end="")
            print(board[row][col].strip().center(9, ' '), end="")
        print("┃")
        pad_row()

    print("┗", end='')
    for col in range(DIM):
        if col > 0:
            draw_tee('┴', col)
        draw_cell_length(True)
    print("┛")


def remove_from_set(cell_set, val):
    return cell_set.replace(val, '')


def populate_full_board():
    board = []
    for row in range(DIM):
        cur_row = []
        for col in range(DIM):
            cur_row.append(FULL_SET)
        board.append(cur_row)
    return board


def puzzle_to_array(puzzle):
    puzzle_array = []
    for i in range(len(puzzle)):
        col = i % DIM
        if col == 0:
            cur_row = []
        cur_row.append(puzzle[i])
        if col == DIM - 1:
            puzzle_array.append(cur_row)
    return puzzle_array


def draw_puzzle(puzzle):
    puzzle_array = puzzle_to_array(puzzle)

    for row in range(DIM):
        for col in range(DIM):
            if col == 0:
                print()

            c = ord(puzzle_array[row][col]) - ord('0')
            if c == 0:
                print("  ", end="")
            else:
                print(" %d" % c, end="")
    print()


def is_solved(cell):
    return(len(cell.strip()) == 1)


def initialize_board(board, puzzle_array):
    for row in range(DIM):
        for col in range(DIM):
            p = puzzle_array[row][col]
            c = ord(p) - ord('0')
            if c > 0:
                for m in FULL_SET:
                    if m == p:
                        continue
                    board[row][col] = remove_from_set(board[row][col], m)


def remove_solved(board):
    reduced = 0
    for row in range(DIM):
        for col in range(DIM):
            cell = board[row][col]
            if is_solved(cell):
                continue

            sg_row = math.floor(row / BASIS) * BASIS
            sg_col = math.floor(col / BASIS) * BASIS
            for r in range(BASIS):
                for c in range(BASIS):
                    reduced = reduced + compare_and_reduce(
                        board, (row, col), (sg_row + r, sg_col + c))
            for r in range(DIM):
                reduced = reduced + compare_and_reduce(
                    board, (row, col), (r, col))
            for c in range(DIM):
                reduced = reduced + compare_and_reduce(
                    board, (row, col), (row, c))
    return reduced


def compare_and_reduce(board, target, other):
    if(target == other):
        return 0
    other_cell = board[other[0]][other[1]]
    target_cell = board[target[0]][target[1]]
    if is_solved(target_cell):
        return 0
    if is_solved(other_cell):
        cell = remove_from_set(target_cell, other_cell.strip())
        assert(len(cell.strip()) != 0)
        board[target[0]][target[1]] = cell
        if target_cell != cell:
            print("removing %s from %s" % (other_cell, target_cell))
            return 1
    return 0


def solve_puzzle(puzzle):
    board = populate_full_board()
    puzzle_array = puzzle_to_array(puzzle)
    initialize_board(board, puzzle_array)
    reduced = remove_solved(board)
    while reduced > 0:
        print("number reduce was %d" % reduced)
        reduced = remove_solved(board)

    return board


def test_anything():
    assert(False)

draw_puzzle(samples.sample_puzzle)
board = solve_puzzle(samples.sample_puzzle)
draw_board(board)
