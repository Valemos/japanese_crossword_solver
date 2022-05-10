import itertools
from dataclasses import dataclass, field

import numpy as np

from crossword.block_direction import Direction


@dataclass
class ACrosswordHints:
    hints: list[list[int]] = field(default_factory=list)

    def __len__(self):
        return len(self.hints)

    def __iter__(self):
        return iter(self.hints)

    def __getitem__(self, key):
        return self.hints[0]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hints == other.hints
        return False


@dataclass
class CrosswordHintsHorizontal(ACrosswordHints):
    def get_row_hints_list(self):
        elem_len = max(map(len, map(str, itertools.chain(*self.hints))))
        return [' '.join(map(lambda el: str(el).rjust(elem_len, ' '), row))
                for row in self.hints]

    @classmethod
    def scan_array(cls, arr):
        new_hints_list = []
        for row in range(arr.shape[0]):
            new_hints_list.append(list(cls.scan_row(arr, row)))

        return cls(new_hints_list)

    @classmethod
    def scan_row(cls, arr, row):
        current_value = 0
        for col in range(arr.shape[1]):
            if arr[row, col] == 1:
                current_value += 1
            elif current_value != 0:
                yield current_value
        if current_value != 0:
            yield current_value


@dataclass
class CrosswordHintsVertical(ACrosswordHints):
    def get_header_str(self):
        max_len = max(map(len, self.hints))

        max_elem_len = max(map(len, map(str, itertools.chain(*self.hints))))
        placeholder = ' ' * max_elem_len

        hints_reversed = list(map(list, map(reversed, self.hints)))

        rows = []
        for row_i in range(max_len):
            rows.append("|")
            for column in hints_reversed:
                if row_i < len(column):
                    element = str(column[row_i]).rjust(max_elem_len)
                else:
                    element = placeholder
                rows[-1] += element + '|'

        return '\n'.join(reversed(rows))

    @classmethod
    def scan_array(cls, arr):
        new_hints_list = []
        for col in range(arr.shape[1]):
            new_hints_list.append(list(cls.scan_column(arr, col)))

        return cls(new_hints_list)

    @classmethod
    def scan_column(cls, arr, col):
        current_value = 0
        for row in range(arr.shape[0]):
            if arr[row, col] == 1:
                current_value += 1
            elif current_value != 0:
                yield current_value
                current_value = 0
        if current_value != 0:
            yield current_value
