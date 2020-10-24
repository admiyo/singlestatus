#!/bin/python
import math
from singlestatus import samples
from singlestatus import display

from singlestatus import common


def remove_from_set(cell_set, val):
    return cell_set.replace(val, '')


def populate_full_board():
    board = []
    for row in range(common.DIM):
        cur_row = []
        for col in range(common.DIM):
            cur_row.append(common.FULL_SET)
        board.append(cur_row)
    return board


def is_solved(cell):
    return(len(cell.strip()) == 1)


def initialize_board(board, puzzle_array):
    for row in range(common.DIM):
        for col in range(common.DIM):
            p = puzzle_array[row][col]
            c = ord(p) - ord('0')
            if c > 0:
                for m in common.FULL_SET:
                    if m == p:
                        continue
                    board[row][col] = remove_from_set(board[row][col], m)


def remove_solved(board):
    reduced = 0
    for row in range(common.DIM):
        for col in range(common.DIM):
            cell = board[row][col]
            if is_solved(cell):
                continue

            sg_row = math.floor(row / common.BASIS) * common.BASIS
            sg_col = math.floor(col / common.BASIS) * common.BASIS
            for r in range(common.BASIS):
                for c in range(common.BASIS):
                    reduced = reduced + compare_and_reduce(
                        board, (row, col), (sg_row + r, sg_col + c))
            for r in range(common.DIM):
                reduced = reduced + compare_and_reduce(
                    board, (row, col), (r, col))
            for c in range(common.DIM):
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
    puzzle_array = common.puzzle_to_array(puzzle)
    initialize_board(board, puzzle_array)
    reduced = remove_solved(board)
    while reduced > 0:
        print("number reduce was %d" % reduced)
        reduced = remove_solved(board)

    return board

display.draw_puzzle(samples.sample_puzzle)
board = solve_puzzle(samples.sample_puzzle)
display.draw_board(board)
