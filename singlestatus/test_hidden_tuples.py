from singlestatus import common
from singlestatus import sudoku
import math

puzzle_bl = ("000374200" +
             "000082040" +
             "000000000" +
             "000030826" +
             "600090004" +
             "805046970" +
             "547020009" +
             "000000405" +
             "010450702")

puzzle = ("632145978" +
          "810090004" +
          "040080010" +
          "000850000" +
          "160274000" +
          "000960000" +
          "481529060" +
          "753416009" +
          "296738040")


board_rc = [["6", "3", "2", "1", "4", "5", "9", "7", "8"],
            ["8", "1", "57", "36", "9", "27", "2356", "235", "4"],
            ["59", "4", "579", "36", "8", "27", "2356", "1", "3256"],
            ["39", "27", "49", "8", "5", "13", "12467", "29", "1267"],
            ["1", "6", "589", "2", "7", "4", "358", "3589", "35"],
            ["35", "27", "458", "9", "6", "13", "124578", "258", "1257"],
            ["4", "8", "1", "5", "2", "9", "73", "6", "73"],
            ["7", "5", "3", "4", "1", "6", "28", "28", "9"],
            ["2", "9", "6", "7", "3", "8", "15", "4", "15"]]


board_bl = [['19', '5689', '1689', '3', '7', '4', '2', '1569', '18'],
            ['1379', '35679', '1369', '1569', '8', '2', '1356', '4', '137'],
            ['123479', '2356789', '1234689', '1569', '16', '159', '1356',
             '13569', '1378'],
            ['1479', '79', '149', '157', '3', '157', '8', '2', '6'],
            ['6', '237', '123', '1278', '9', '178', '135', '135', '4'],
            ['8', '23', '5', '12', '4', '6', '9', '7', '13'],
            ['5', '4', '7', '168', '2', '138', '136', '1368', '9'],
            ['239', '23689', '23689', '16789', '16', '13789', '4', '1368',
             '5'],
            ['39', '1', '3689', '4', '5', '389', '7', '368', '2']]


def test_gen_subsets():
    allset = ['a', 'e', 'i', 'o', 'u']
    sudoku.gen_subsets(allset, 3)


def test_gen_subset_indexes():
    subsets = sudoku.gen_subset_indexes(9, 4)
    combos = math.factorial(9) / (
        (math.factorial(5) * math.factorial(4)))

    for s in subsets:
        print(s)
    assert(len(subsets) == combos)


def test_board_cell_iterator():
    board = sudoku.populate_full_board()
    puzzle_array = common.puzzle_to_array(puzzle)
    sudoku.initialize_board(board, puzzle_array)
    itr = sudoku.BoardCellIterator(board)
    assert(itr.__next__().get() == '6')


def test_append_to_tuple_map():
    tuple_map = dict()
    tuple = '5689'
    sudoku.append_to_tuple_map(tuple_map, 0, 0, tuple, board_bl)
    sudoku.append_to_tuple_map(tuple_map, 0, 1, tuple, board_bl)
    key = sudoku.TupleKey('r', 0, '5689')
    key.__hash__()

    cells = tuple_map[key]
    assert(cells is not None)
    assert(len(cells) == 2)


def test_block_for_rc():
    assert([0, 0] == sudoku.block_for_rc(0, 0))
    assert([2, 2] == sudoku.block_for_rc(8, 8))
    assert([1, 2] == sudoku.block_for_rc(3, 6))
    assert([1, 2] == sudoku.block_for_rc(5, 8))
    assert([1, 1] == sudoku.block_for_rc(4, 4))


def test_gen_tuple_map():
    tuple_map = sudoku.generate_hidden_tuple_map(board_bl, 4)
    key = sudoku.TupleKey('c', 1, '5678')
    assert('5' in '5678')

    cells = tuple_map[key]
    assert(cells is not None)
    assert(len(cells) == 6)

    key = sudoku.TupleKey('c', 1, '5689')
    cells = tuple_map[key]
    assert(len(cells) == 5)

    key = sudoku.TupleKey('c', 1, '3568')
    cells = tuple_map[key]
    assert(len(cells) == 6)

    tuple_map = sudoku.generate_hidden_tuple_map(board_rc, 4)
    key = sudoku.TupleKey('b', [1, 2], '1467')
    cells = tuple_map[key]
    assert(len(cells) == 4)
    assert([(3, 6), (3, 8), (5, 6), (5, 8)] == cells)


def test_gen_tuples():
    subsets = sudoku.gen_subsets(common.FULL_SET, 4)
    combos = math.factorial(9) / (
        (math.factorial(5) * math.factorial(4)))
    assert(len(subsets) == combos)


def test_find_hidden_tuples():
    found = sudoku.find_hidden_tuples(board_rc, 4)
    assert(8 == len(found))

    found = sudoku.find_hidden_tuples(board_bl, 4)
    assert(7 == len(found))


def test_reduce_hidden_tuples():
    board = board_bl
    sudoku.find_and_reduce_hidden_tuples(board, 4)
    sudoku.reduce_solved(board)

    assert(board[2][8] == "78")
