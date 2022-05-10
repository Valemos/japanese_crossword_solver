import itertools
from typing import Generator

import numpy as np

import copy

from .direction import Direction
from .cell_block_set import CellBlockSet
from .crossword_cell import CrosswordCell
from .crossword_hints import CrosswordHintsVertical, CrosswordHintsHorizontal


class CrosswordSolution:
    """
     |1|3|1|
    2|*|*| |
    1| |*| |
    2| |*|*|

    1, 3, 1 - vertical hints
    2, 1, 2 - horizontal hints

    solver uses vertical hints as reference
    and compares solutions with horizontal hints
    """

    def __init__(self, solution):
        self._h_hints = CrosswordHintsHorizontal.scan_array(solution)
        self._v_hints = CrosswordHintsVertical.scan_array(solution)
        self._solution = solution
        self._columns = self._build_columns()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._solution != other._solution:
                return False
            return self._v_hints == other._v_hints and \
                   self._h_hints == other._h_hints and \
                   self._columns == other._columns

    @classmethod
    def from_hints(cls, h_hints, v_hints):
        self = object.__new__(cls)
        self._h_hints = h_hints
        self._v_hints = v_hints
        self._solution = np.zeros((len(self._h_hints), len(self._v_hints)))
        self._columns = self._build_columns()
        for col in self._columns:
            self._add_solution_column(col)
        return self

    def copy(self):
        obj_copy = self.__new__(CrosswordSolution)
        obj_copy._columns = copy.deepcopy(self._columns)
        obj_copy._solution = self._solution.copy()
        obj_copy._v_hints = self._v_hints
        obj_copy._h_hints = self._h_hints
        return obj_copy

    def _build_columns(self):
        columns = []
        for x, col in enumerate(self._v_hints.hints):
            columns.append(CellBlockSet(x, Direction.VERTICAL, col))

        max_row_len = len(self._h_hints)
        for col in columns:
            col.set_max_length(max_row_len)

        return columns

    def get_hint_strings(self):
        col_hints = self._v_hints.get_header_str()
        row_hints = self._h_hints.get_row_hints_list()

        col_elem_len = max(map(len, map(str, itertools.chain(*self._v_hints))))
        row_hint_len = max(map(len, row_hints))
        h_padding = ' ' * row_hint_len

        col_hints = h_padding + col_hints.replace('\n', '\n' + h_padding)
        row_hints = [hint.rjust(row_hint_len, ' ') for hint in row_hints]

        return col_hints, row_hints, col_elem_len

    @classmethod
    def from_string(cls, string):
        """
        acceptable format:
        ' ' - space for empty cell
        '*' - star for filled cell
        '\n' - new line to separate rows
        """
        cells = [list(row) for row in string.split('\n') if len(row.strip()) > 0]

        arr = np.zeros((
            len(cells),
            max(map(len, cells))
        ))
        for x, row in enumerate(cells):
            for y, value in enumerate(row):
                cell = CrosswordCell(value)
                arr[x, y] = cell.to_int()

        return CrosswordSolution(arr)

    def pretty_str(self):
        col_hints, row_hints, col_len = self.get_hint_strings()

        def _to_cell_string(el):
            return CrosswordCell.from_bool(el).value.rjust(col_len, ' ')

        rows = []
        for i, row_hint in enumerate(row_hints):
            values = '|'.join(map(_to_cell_string, self._solution[i, :]))
            rows.append(f"{row_hint}|{values}|")

        all_rows = '\n'.join(rows)
        return f"{col_hints}\n{all_rows}"

    def reset(self):
        return CrosswordSolution.from_hints(self._h_hints, self._v_hints)

    @property
    def movable_columns(self) -> Generator:
        for col in self._columns:
            if not col.is_fixed:
                yield col

    def is_solved(self):
        if self.is_invalid(): return False
        current_h_hints = CrosswordHintsHorizontal.scan_array(self._solution)
        return self._h_hints == current_h_hints

    def set_column(self, col: CellBlockSet):
        self._remove_solution_column(self._columns[col.position])
        self._columns[col.position] = col
        self._add_solution_column(col)

    def is_invalid(self):
        """checks if current crossword cannot exist"""
        for row_i, row_hint in enumerate(self._h_hints.hints):
            scanned_hint = CrosswordHintsHorizontal.scan_row(self._solution, row_i)
            if any(map(lambda tup: tup[0] != tup[1], zip(row_hint, scanned_hint))):
                return True
        return False

    def _add_solution_column(self, col):
        self._set_column_cells(col, 1)

    def _remove_solution_column(self, col):
        self._set_column_cells(col, 0)

    def _set_column_cells(self, col: CellBlockSet, value):
        for row_pos in self._columns[col.position].iter_positions():
            self._solution[row_pos, col.position] = value
