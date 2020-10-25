#!/bin/python
import math
from singlestatus import samples
from singlestatus import display

from singlestatus import common


class Cell:
    def __init__(self, board, r, c):
        self.board = board
        self.r = r
        self.c = c

    def get(self):
        return self.board[self.r][self.c]

    def set(self, val):
        self.board[self.r][self.c] = val

    def is_solved(self):
        return (len(self.get().strip()) == 1)

    def remove_from_set(self, val):
        curr = self.get()
        return curr.replace(val, '')

    def compare_and_reduce(self, other):
        if self.is_solved():
            return 0
        if other.is_solved():
            curr = self.get()
            cell = self.remove_from_set(other.get().strip())
            assert(len(cell.strip()) != 0)
            self.set(cell)
            if curr != cell:
                return 1
        return 0


# Iterates through all the Cells in a given Row
class RowCellIterator:
    def __init__(self, board, row_index):
        self.board = board
        self.row_index = row_index
        self.col = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.col < common.DIM:
            val = Cell(self.board, self.row_index, self.col)
            self.col = self.col + 1
            return val
        else:
            raise StopIteration


# Iterates through all the Cells in a given Column
class ColCellIterator:
    def __init__(self, board, col):
        self.board = board
        self.row = 0
        self.col = col

    def __iter__(self):
        return self

    def __next__(self):
        if self.row < common.DIM:
            val = Cell(self.board, self.row, self.col)
            self.row = self.row + 1
            return val
        else:
            raise StopIteration


# Iterates through all the Cells in the same block
class BlockCellIterator:
    def __init__(self, board, row, col):
        self.board = board
        self.sg_row = math.floor(row / common.BASIS) * common.BASIS
        self.sg_col = math.floor(col / common.BASIS) * common.BASIS
        self.block_row = 0
        self.block_col = 0

    def get_row(self):
        return self.sg_row + self.block_row

    def get_col(self):
        return self.sg_col + self.block_col

    def __iter__(self):
        return self

    def __next__(self):
        if self.block_row >= common.BASIS:
            raise StopIteration
        cell = Cell(self.board, self.get_row(), self.get_col())
        self.block_col = self.block_col + 1

        if (self.block_col >= common.BASIS):
            self.block_col = 0
            self.block_row = self.block_row + 1
        return cell


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

            target = Cell(board, row, col)
            for other in BlockCellIterator(board, row, col):
                reduced = reduced + target.compare_and_reduce(other)

            for other in ColCellIterator(board, col):
                reduced = reduced + target.compare_and_reduce(other)

            for other in RowCellIterator(board, row):
                reduced = reduced + target.compare_and_reduce(other)
    return reduced


def solve_puzzle(puzzle):
    board = populate_full_board()
    puzzle_array = common.puzzle_to_array(puzzle)
    initialize_board(board, puzzle_array)
    reduced = remove_solved(board)
    while reduced > 0:
        reduced = remove_solved(board)
    return board

display.draw_puzzle(samples.sample_puzzle)
sample_board = solve_puzzle(samples.sample_puzzle)
display.draw_board(sample_board)
