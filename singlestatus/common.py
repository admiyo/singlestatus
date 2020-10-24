BASIS = 3
DIM = BASIS * BASIS
FULL_SET = "123456789"


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
