#!/bin/python
import math
import json
from singlestatus import samples
from singlestatus import display

from singlestatus import common


class Cell:
    def __init__(self, board, r, c):
        self.board = board
        self.r = r
        self.c = c

    def __eq__(self, other):
        assert(isinstance(other, Cell))
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
        if self.is_solved():
            return 0
        for other in BlockCellIterator(self.board, self.r, self.c):
            reduced = reduced + self.compare_and_reduce(other)
        for other in ColCellIterator(self.board, self.c):
            reduced = reduced + self.compare_and_reduce(other)
        for other in RowCellIterator(self.board, self.r):
            reduced = reduced + self.compare_and_reduce(other)
        return reduced


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


# Iterates through all the Cells one the board
class BoardCellIterator:
    def __init__(self, board):
        self.board = board
        self.row = 0
        self.col = 0

    def reset(self):
        self.col = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.col == common.DIM:
            self.col = 0
            self.row += 1
        if self.row == common.DIM:
            raise StopIteration
        val = Cell(self.board, self.row, self.col)
        self.col += 1
        return val


def block_for_rc(row, col):
    sg_row = math.floor(row / common.BASIS)
    sg_col = math.floor(col / common.BASIS)
    return [sg_row, sg_col]


# select k from n.  Number of elements will be
# n!/(k! - (n-k)!)
def gen_subset_indexes(n, k):
    subsets = []
    max = 1 << n
    for i in range(max):
        indexes = []
        for x in range(9):
            if (i >> x) & 1 == 1:
                indexes.append(x)
        if len(indexes) == k:
            subsets.append(indexes)
    return subsets


# generates all subsets of length k
def gen_subsets(allset, k):
    subsets = []
    indexes = gen_subset_indexes(len(allset), k)
    for i in indexes:
        subset = []
        for j in i:
            subset.append(allset[j])
        subsets.append(subset)
    return subsets


class TupleKey:
    def __init__(self, house, location, tuple):
        self.house = house
        self.location = location
        self.tuple = tuple

    def __eq__(self, other):
        if not isinstance(other, TupleKey):
            return False
        return ((self.house == other.house) and
                (self.location == other.location) and
                (self.tuple == other.tuple))

    def __hash__(self):
        return hash(self.__str__())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s %s %s" % (self.house, self.location, self.tuple)


def append_to_tuple_map(tuple_map, r, c, tuple, board):
    def no_singletons(board, itr):
        ok = True
        for cell in itr:
            if not ok:
                break
            for digit in tuple:
                if cell.get() == digit:
                    ok = False
                    break
        return ok

    tuple_str = ""
    for i in tuple:
        tuple_str += i
    keys = []

    if no_singletons(board, RowCellIterator(board, r)):
        keys.append(TupleKey('r', r, tuple_str))

    if no_singletons(board, ColCellIterator(board, c)):
        keys.append(TupleKey('c', c, tuple_str))

    if no_singletons(board, BlockCellIterator(board, r, c)):
        keys.append(TupleKey('b', block_for_rc(r, c), tuple_str))

    for key in keys:
        if tuple_map.get(key) is None:
            tuple_map[key] = []
        tuple_map[key].append((r, c))


def generate_hidden_tuple_map(board, k):
    tuples = gen_subsets(common.FULL_SET, k)
    tuple_map = dict()
    for cell in BoardCellIterator(board):
        if len(cell.get()) == 1:
            continue
        for tuple in tuples:
            for digit in tuple:
                if digit in cell.get():
                    append_to_tuple_map(
                        tuple_map, cell.r, cell.c, tuple, board)
                    break
    return tuple_map


def find_hidden_tuples(board, k):
    tuple_map = generate_hidden_tuple_map(board, k)
    found = dict()
    for (key, values) in tuple_map.items():
        if len(values) == k:
            found[key] = values
    return found


def reduce_hidden_tuples(board, found, n):
    for (key, cells) in found.items():
        digits_in = key.tuple
        digits_out = common.FULL_SET
        for c in digits_in:
            digits_out = digits_out.replace(c, '')

        itr = None
        if key.house == 'b':
            itr = BlockCellIterator(board, cells[0][0], cells[0][1])
        elif key.house == 'r':
            itr = RowCellIterator(board, cells[0][0])
        elif key.house == 'c':
            itr = ColCellIterator(board, cells[0][1])
        else:
            assert(itr is not None)

        for cell in itr:
            ct = (cell.r, cell.c)
            if ct in cells:
                cell.set(cell.remove_from_set(digits_out))
            else:
                cell.set(cell.remove_from_set(digits_in))


def find_and_reduce_hidden_tuples(board, n):
    found = find_hidden_tuples(board, n)
    reduce_hidden_tuples(board, found, n)


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


def reduce_singleton_in_section(itr, test_val):
    found = None
    for other in itr:
        if other.contains(test_val):
            if found is None:
                found = other
            else:
                found = None
                return
    if found is not None:
        found.solve("%d" % test_val)


def reduce_singletons_in_section(itr):
    for test_val in range(common.DIM):
        reduce_singleton_in_section(itr, test_val)
        itr.reset()


def reduce_naked_pairs_in_section(itr):
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
    visit_all(board, reduce_singletons_in_section)


def reduce_naked_pairs(board):
    visit_all(board, reduce_naked_pairs_in_section)


def visit_all(board, visitor):
    for col in range(common.DIM):
        visitor(ColCellIterator(board, col))

    for row in range(common.DIM):
        visitor(RowCellIterator(board, row))

    for r in range(common.BASIS):
        for c in range(common.BASIS):
            visitor(
                BlockCellIterator(board, r * common.BASIS, c * common.BASIS))


def x_wing(board):
    xmap = dict()
    for row in range(common.DIM):
        valmap = dict()
        for cell in RowCellIterator(board, row):
            if cell.is_solved():
                continue
            for val in cell.get():
                if valmap.get(val) is None:
                    valmap[val] = []
                valmap[val].append(cell)
        xmap[row] = valmap

    pairs_by_val = dict()
    for row, matches in xmap.items():
        for val, cells in matches.items():
            if (len(cells)) == 2:
                if pairs_by_val.get(val) is None:
                    pairs_by_val[val] = []
                pairs_by_val[val].append(cells)

    reduced = 0
    for val, rows in pairs_by_val.items():
        pos_dict = dict()
        for r in rows:
            tup = (r[0].c, r[1].c)
            o = pos_dict.get(tup)
            if o is None:
                pos_dict[tup] = r
            else:
                for mc in r:
                    for target in ColCellIterator(board, mc.c):
                        if target.r == r[0].c:
                            continue
                        if target.r == r[1].c:
                            continue
                        if target.r == o[0].c:
                            continue
                        if target.r == o[1].c:
                            continue
                        if val in target.get():
                            target.set(target.remove_from_set(val))
                            reduced = reduced + 1 + target.reduce_solved()
    return reduced


def solve_puzzle(puzzle):
    board = populate_full_board()
    puzzle_array = common.puzzle_to_array(puzzle)
    initialize_board(board, puzzle_array)
    reduced = reduce_solved(board)
    reduced = 10
    while reduced > 0:
        reduced = reduced - 1
        #x_wing(board)
        reduce_naked_pairs(board)
        reduce_singletons(board)
        reduced = reduce_solved(board)
        find_and_reduce_hidden_tuples(board, 4)

    return board


def solve_sample():
    display.draw_puzzle(samples.sample_puzzle)
    sample_board = solve_puzzle(samples.sample_puzzle)
    display.draw_board(sample_board)


def solve_from_file():
    solved_map = dict()
    infile = open("data/sample_sudoku_board_inputs.csv")
    line = infile.readline()
    for line in infile:
        solved_map[line] = solve_puzzle(line)
    print(json.dumps(solved_map))


solve_from_file()
#solve_sample()
