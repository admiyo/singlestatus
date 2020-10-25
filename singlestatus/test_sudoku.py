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
    assert(target_cell.get() == '12345678')
    assert(count == 1)

    count = other_cell.compare_and_reduce(other_cell)
    assert(other_cell.get() == '9')
    assert(count == 0)

    other_cell = sudoku.Cell(board, 7, 0)
    assert(other_cell.get() == common.FULL_SET)

    count = target_cell.compare_and_reduce(other_cell)
    assert(target_cell.get() == '12345678')
    assert(count == 0)


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
