import numpy as np

import copy

from .cell_block import CellBlock
from .block_direction import BlockDirection
from .cell_block_set import CellBlockSet
from .crossword_cell import CrosswordCell
from .crossword_hints import CrosswordHints


class CrosswordSolution:
    def __init__(self, hints, solution=None):
        self._hints: CrosswordHints = hints
        self._solution: np.ndarray = solution \
            if solution is not None else \
            np.zeros(hints.shape)
        self._columns, self._rows = self._build_rectangles()

    def _build_rectangles(self):
        columns = []
        for x, col in enumerate(self._hints.horizontal):
            columns.append(CellBlockSet(x, BlockDirection.VERTICAL, col))

        rows = []
        for y, row in enumerate(self._hints.vertical):
            rows.append(CellBlockSet(y, BlockDirection.HORIZONTAL, row))

        max_row_len = max(map(lambda b: b.length, columns))
        max_column_len = max(map(lambda b: b.length, rows))

        for col in columns:
            col.set_max_length(max_row_len)

        for row in rows:
            row.set_max_length(max_column_len)

        return columns, rows

    def pretty_str(self):
        col_hints, row_hints, col_len = self._hints.get_hint_strings()

        def _to_cell_string(el):
            return CrosswordCell.from_bool(el).value.rjust(col_len, ' ')

        rows = []
        for i, row_hint in enumerate(row_hints):
            values = '|'.join(map(_to_cell_string, self._solution[i, :]))
            rows.append(f"{row_hint}|{values}|")

        all_rows = '\n'.join(rows)
        return f"{col_hints}\n{all_rows}"

    def reset(self):
        self._solution = np.zeros(self._solution.shape)

    @property
    def columns(self) -> list[CellBlockSet]:
        return self._columns

    @property
    def rows(self):
        return self._rows

    def is_solved(self):
        return all(block.is_solved() for block in (*self._columns, *self._rows))

    def set_column(self, col: CellBlockSet):
        self._columns[col.position] = col

    def is_invalid(self):
        max_col, max_row = self._hints.shape
        for col_i in range(max_col):
            for row_i in range(max_row):
                if not (self._columns[col_i].contains_point(col_i, row_i) and
                        self._rows[row_i].contains_point(col_i, row_i)):
                    return False
        return True

    def copy(self):
        obj_copy = copy.deepcopy(self)
        obj_copy._hints = self._hints
        return obj_copy
