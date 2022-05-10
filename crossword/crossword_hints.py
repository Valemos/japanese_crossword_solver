import itertools
from dataclasses import dataclass


@dataclass
class CrosswordHints:
    horizontal: list[list[int]]
    vertical: list[list[int]]

    @property
    def shape(self):
        return len(self.horizontal), len(self.vertical)

    def get_horizontal_str(self):
        max_len = max(map(len, self.horizontal))

        max_elem_len = max(map(len, map(str, itertools.chain(*self.horizontal))))
        placeholder = ' ' * max_elem_len

        horizontal_reversed = list(map(list, map(reversed, self.horizontal)))

        rows = []
        for row_i in range(max_len):
            rows.append("|")
            for column in horizontal_reversed:
                if row_i < len(column):
                    element = str(column[row_i]).rjust(max_elem_len)
                else:
                    element = placeholder
                rows[-1] += element + '|'

        return '\n'.join(reversed(rows))

    def get_vertical_hints_list(self):
        v_elem_len = max(map(len, map(str, itertools.chain(*self.vertical))))
        return [' '.join(map(lambda el: str(el).rjust(v_elem_len, ' '), row))
                for row in self.vertical]

    def get_hint_strings(self):
        h_hints = self.get_horizontal_str()
        v_hints = self.get_vertical_hints_list()

        h_elem_len = max(map(len, map(str, itertools.chain(*self.horizontal))))
        v_row_len = max(map(len, v_hints))
        h_padding = ' ' * v_row_len

        h_hints = h_padding + h_hints.replace('\n', '\n' + h_padding)
        v_hints = [hint.rjust(v_row_len, ' ') for hint in v_hints]

        return h_hints, v_hints, h_elem_len
