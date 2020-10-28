from singlestatus import common
from singlestatus import samples
from singlestatus import sudoku


simple_solution = [['5', '3', '4', '6', '7', '8', '9', '1', '2'],
                   ['6', '7', '2', '1', '9', '5', '3', '4', '8'],
                   ['1', '9', '8', '3', '4', '2', '5', '6', '7'],
                   ['8', '5', '9', '7', '6', '1', '4', '2', '3'],
                   ['4', '2', '6', '8', '5', '3', '7', '9', '1'],
                   ['7', '1', '3', '9', '2', '4', '8', '5', '6'],
                   ['9', '6', '1', '5', '3', '7', '2', '8', '4'],
                   ['2', '8', '7', '4', '1', '9', '6', '3', '5'],
                   ['3', '4', '5', '2', '8', '6', '1', '7', '9']]

simple_solution_col = ['5', '6', '1', '8', '4', '7', '9', '2', '3']
simple_solution_first_block = ['5', '3', '4', '6', '7', '2', '1', '9', '8']
simple_solution_final_block = ['2', '8', '4', '6', '3', '5', '1', '7', '9']


def test_hello_world():
    board = sudoku.solve_puzzle(samples.simple_puzzle)
    assert(board == simple_solution)


def test_cell_compare_and_reduce():
    board = sudoku.populate_full_board()
    puzzle_array = common.puzzle_to_array(samples.simple_puzzle)
    sudoku.initialize_board(board, puzzle_array)
    target_cell = sudoku.Cell(board, 0, 8)
    assert(target_cell.get() == common.FULL_SET)
    other_cell = sudoku.Cell(board, 8, 8)
    assert(other_cell.get() == '9')

    count = target_cell.compare_and_reduce(other_cell)
    assert(target_cell.get() == '248')
    assert(count == 6)

    count = other_cell.compare_and_reduce(other_cell)
    assert(other_cell.get() == '9')
    assert(count == 0)

    other_cell = sudoku.Cell(board, 7, 0)
    assert(other_cell.get() == common.FULL_SET)

    count = target_cell.compare_and_reduce(other_cell)
    assert(target_cell.get() == '248')
    assert(count == 0)


def test_contains():
    board = sudoku.populate_full_board()
    puzzle_array = common.puzzle_to_array(samples.simple_puzzle)
    sudoku.initialize_board(board, puzzle_array)
    target_cell = sudoku.Cell(board, 0, 8)
    assert(target_cell.get() == common.FULL_SET)
    assert(target_cell.contains(1))
    assert(target_cell.contains(9))

    other_cell = sudoku.Cell(board, 8, 8)
    assert(not other_cell.contains(1))
    assert(other_cell.contains(9))


def test_reduce_singletons_positive():
    test_val = 4
    test_str = "%d" % test_val
    test_set = common.FULL_SET.replace(test_str, '')

    board = sudoku.populate_full_board()
    for c in range(1, 9):
        board[0][c] = test_set
    assert(board[0][1] == test_set)

    itr = sudoku.RowCellIterator(board, 0)
    sudoku.reduce_singleton_in_section(itr, test_val)
    assert(board[0][0] == test_str)
    for c in range(1, 9):
        assert(board[0][c] == test_set)


def test_reduce_singletons_none():
    test_val = 4
    test_set = common.FULL_SET
    board = sudoku.populate_full_board()
    itr = sudoku.RowCellIterator(board, 0)
    sudoku.reduce_singleton_in_section(itr, test_val)
    for c in range(0, 9):
        assert(board[0][c] == test_set)


def test_reduce_naked_pairs_postitive():
    test_set = "3456789"
    board = sudoku.populate_full_board()
    board[0][0] = "12"
    board[0][8] = "12"
    itr = sudoku.RowCellIterator(board, 0)
    sudoku.reduce_naked_pairs_in_section(itr)
    for c in range(1, 8):
        assert(board[0][c] == test_set)


def test_cell_get():
    board = common.puzzle_to_array(samples.simple_puzzle)
    cell = sudoku.Cell(board, 8, 8)
    assert(cell.get() == '9')


def test_row_cell_itr():
    board = simple_solution
    itr = sudoku.RowCellIterator(board, 0)
    results = []
    for x in itr:
        results.append(x.get())
    assert(results == simple_solution[0])


def test_col_cell_itr():
    board = simple_solution
    itr = sudoku.ColCellIterator(board, 0)
    results = []
    for x in itr:
        results.append(x.get())
    assert(results == simple_solution_col)


def test_block_cell_itr():
    board = simple_solution
    itr = sudoku.BlockCellIterator(board, 1, 1)
    results = []
    for x in itr:
        results.append(x.get())
    assert(results == simple_solution_first_block)

    itr = sudoku.BlockCellIterator(board, 8, 8)
    results = []
    for x in itr:
        results.append(x.get())
    assert(results == simple_solution_final_block)


def test_xwing():
    xwingboard = [["2467", "2479", "3", "8", "469", "24", "5", "1", "46"],
                  ["2456", "245", "8", "7", "146", "124", "9", "3", "46"],
                  ["1", "49", "69", "3", "469", "5", "7", "2", "8"],
                  ["567", "357", "567", "1", "137", "13", "8", "4", "9"],
                  ["8", "34", "1", "9", "34", "6", "2", "5", "7"],
                  ["247", "2479", "79", "5", "478", "48", "1", "6", "3"],
                  ["9", "6", "4", "1", "2", "7", "3", "8", "5"],
                  ["3", "8", "2", "6", "5", "9", "4", "7", "1"],
                  ["57", "1", "57", "4", "38", "38", "6", "9", "2"]]

    xw_reduced = [["2467", "279", "3", "8", "69", "24", "5", "1", "46"],
                  ["2456", "245", "8", "7", "46", "24", "9", "3", "46"],
                  ["1", "9", "69", "3", "6", "5", "7", "2", "8"],
                  ["567", "357", "567", "1", "37", "3", "8", "4", "9"],
                  ["8", "34", "1", "9", "34", "6", "2", "5", "7"],
                  ["247", "27", "79", "5", "78", "48", "1", "6", "3"],
                  ["9", "6", "4", "1", "2", "7", "3", "8", "5"],
                  ["3", "8", "2", "6", "5", "9", "4", "7", "1"],
                  ["57", "1", "57", "4", "3", "3", "6", "9", "2"]]

    sudoku.x_wing(xwingboard)

    assert(xwingboard == xw_reduced)
