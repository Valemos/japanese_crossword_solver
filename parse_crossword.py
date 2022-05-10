import numpy as np

from crossword.crossword_cell import CrosswordCell
from crossword.crossword_hints import CrosswordHints
from crossword.crossword_solution import CrosswordSolution


def from_link(link):
    size_str, values_str = link.split(':', maxsplit=1)
    size = list(map(int, size_str.split('x')))
    print(size)

    def _transform_row(row_str):
        return list(map(int, row_str.split('.')))

    values_list = list(map(_transform_row, values_str.split('/')))
    h_hints, v_hints = values_list[:size[0]], values_list[size[0]:]

    hints = CrosswordHints(h_hints, v_hints)
    return CrosswordSolution(hints)


def create_from_string(string):
    cells = [list(row) for row in string.split('\n') if len(row.strip()) > 0]

    arr = np.zeros((
        len(cells),
        max(map(len, cells))
    ))
    for x, row in enumerate(cells):
        for y, value in enumerate(row):
            cell = CrosswordCell(value)
            arr[x, y] = 1 if cell == CrosswordCell.ACTIVE else 0

    v_hints = []
    for x in range(arr.shape[0]):
        hints = [0]
        for y in range(arr.shape[1]):
            if arr[x, y] == 1:
                hints[-1] += 1
            elif hints[-1] != 0:
                hints.append(0)
        while hints[-1] == 0: hints.pop(-1)
        v_hints.append(hints)

    h_hints = []
    for y in range(arr.shape[1]):
        hints = [0]
        for x in range(arr.shape[0]):
            if arr[x, y] == 1:
                hints[-1] += 1
            elif hints[-1] != 0:
                hints.append(0)
        while hints[-1] == 0: hints.pop(-1)
        h_hints.append(hints)

    hints = CrosswordHints(h_hints, v_hints)
    return CrosswordSolution(hints, arr)
