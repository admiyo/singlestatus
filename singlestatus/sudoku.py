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

    def __eq__(self, other):
        return ((self.board == other.board)
                and (self.r == other.r)
                and (self.c == other.c))

    def get(self):
        return self.board[self.r][self.c]

    def contains(self, val):
        return self.get().find("%d" % val) > -1

    def set(self, val):
        self.board[self.r][self.c] = val

    def is_solved(self):
        return (len(self.get().strip()) == 1)

    def remove_from_set(self, vals):
        curr = self.get()
        for c in vals:
            curr = curr.replace(c, '')
        return curr

    def compare_and_reduce(self, other):
        if self.is_solved():
            return 0
        if other.is_solved():
            curr = self.get()
            cell = self.remove_from_set(other.get().strip())
            assert(len(cell.strip()) != 0)
            self.set(cell)
            if curr != cell:
                reduced = 1 + self.reduce_solved()
                return reduced
        return 0

    def solve(self, p):
        if self.is_solved():
            return
        solve_set = common.FULL_SET.replace(p, '')
        self.set(self.remove_from_set(solve_set))
        self.reduce_solved()

    def reduce_solved(self):
        reduced = 0
        row = self.r
        col = self.c
        board = self.board
        if self.is_solved():
            return 0
        for other in BlockCellIterator(board, row, col):
            reduced = reduced + self.compare_and_reduce(other)
        for other in ColCellIterator(board, col):
            reduced = reduced + self.compare_and_reduce(other)
        for other in RowCellIterator(board, row):
            reduced = reduced + self.compare_and_reduce(other)
        return reduced


class BoardCellIterator:
    def __init__(self, board):
        self.board = board
        self.row = 0
        self.col = 0

    def reset(self):
        self.col = 0
        self.row = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.row >= common.DIM:
            raise StopIteration
        val = Cell(self.board, self.row, self.col)
        self.col = self.col + 1
        if self.col >= common.DIM:
            self.col = 0
            self.row = self.row + 1
        return val


# Iterates through all the Cells in a given Row
class RowCellIterator:
    def __init__(self, board, row):
        self.board = board
        self.row = row
        self.col = 0

    def reset(self):
        self.col = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.col < common.DIM:
            val = Cell(self.board, self.row, self.col)
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

    def reset(self):
        self.row = 0

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

    def reset(self):
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


def remove_from_set(cell_set, vals):
    for c in vals:
        cell_set = cell_set.replace(c, '')
    return cell_set


def populate_full_board():
    board = []
    for row in range(common.DIM):
        cur_row = []
        for col in range(common.DIM):
            cur_row.append(common.FULL_SET)
        board.append(cur_row)
    return board


def initialize_board(board, puzzle_array):
    for cell in BoardCellIterator(board):
        p = puzzle_array[cell.r][cell.c]
        if p > '0':
            cell.solve(p)


def reduce_solved(board):
    reduced = 0
    for target in BoardCellIterator(board):
        reduced = reduced + target.reduce_solved()
    return reduced


def reduce_singletons_in_section(itr, test_val):
    found = None
    for other in itr:
        if other.contains(test_val):
            if found is None:
                found = other
            else:
                found = None
                return
    if found is not None:
        found.set("%d" % test_val)


def reduce_matched_pairs_in_section(itr):
    firsts = {}
    second = None

    for cell in itr:
        val = cell.get()
        if len(val) == 2:
            if firsts.get(val) is None:
                firsts[val] = cell
            else:
                second = cell
                break
    if second is None:
        return
    val = second.get()
    first = firsts[val]
    itr.reset()
    for cell in itr:
        if cell == first:
            continue
        if cell == second:
            continue
        new_value = cell.remove_from_set(val)
        cell.set(new_value)


def reduce_singletons(board):
    for col in range(common.DIM):
        for test_val in range(common.DIM):
            reduce_singletons_in_section(ColCellIterator(board, col), test_val)

    for row in range(common.DIM):
        for test_val in range(common.DIM):
            reduce_singletons_in_section(RowCellIterator(board, row), test_val)

    for r in range(common.BASIS):
        for c in range(common.BASIS):
            for test_val in range(common.DIM):
                reduce_singletons_in_section(
                    BlockCellIterator(
                        board, r * common.BASIS, c * common.BASIS),
                    test_val)


def reduce_matched_pairs(board):
    for col in range(common.DIM):
        reduce_matched_pairs_in_section(ColCellIterator(board, col))

    for row in range(common.DIM):
        reduce_matched_pairs_in_section(RowCellIterator(board, row))

    for r in range(common.BASIS):
        for c in range(common.BASIS):
            reduce_matched_pairs_in_section(
                BlockCellIterator(board, r * common.BASIS, c * common.BASIS))


def solve_puzzle(puzzle):
    board = populate_full_board()
    puzzle_array = common.puzzle_to_array(puzzle)
    initialize_board(board, puzzle_array)
    reduced = reduce_solved(board)
    while reduced > 0:
        reduce_matched_pairs(board)
        reduce_singletons(board)
        reduced = reduce_solved(board)
    return board

display.draw_puzzle(samples.sample_puzzle)
sample_board = solve_puzzle(samples.hard_puzzle)
display.draw_board(sample_board)
