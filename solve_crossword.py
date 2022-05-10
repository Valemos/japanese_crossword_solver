import parse_crossword
from crossword.crossword_solution import CrosswordSolution


def generate_solutions(initial_crossword: CrosswordSolution):
    crossword = initial_crossword.copy()
    yield crossword

    for column in crossword.columns:
        for possible_position in column.iter_permutations():
            possible_position.fixed = True
            crossword.set_column(possible_position)


def solve(initial_crossword: CrosswordSolution):
    if initial_crossword.is_invalid():
        raise RuntimeError("cannot solve crossword")

    for solution in generate_solutions(initial_crossword):
        if solution.is_solved():
            return solution

    raise RuntimeError("crossword has no solutions")


if __name__ == '__main__':
    cross_string = " ***\n" \
                   "** *\n" \
                   "  **\n" \
                   "****\n" \
                   "****\n" \
                   " ***\n" \
                   "** *\n" \
                   " * *\n"

    cw = parse_crossword.create_from_string(cross_string)
    cw.reset()
    print(cw.pretty_str())
    sl = solve(cw)
    print(sl.pretty_str())
