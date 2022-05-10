from crossword.crossword_hints import CrosswordHintsHorizontal, CrosswordHintsVertical
from crossword.crossword_solution import CrosswordSolution


def from_link(link):
    size_str, values_str = link.split(':', maxsplit=1)
    size = list(map(int, size_str.split('x')))
    print(size)

    def _transform_row(row_str):
        return list(map(int, row_str.split('.')))

    values_list = list(map(_transform_row, values_str.split('/')))
    h_hints = CrosswordHintsHorizontal(values_list[size[0]:])
    v_hints = CrosswordHintsVertical(values_list[:size[0]])
    return CrosswordSolution.from_hints(h_hints, v_hints)
