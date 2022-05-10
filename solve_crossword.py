import parse_crossword
from crossword.crossword_solution import CrosswordSolution


def generate_solutions(crossword: CrosswordSolution):
    for column in sorted(crossword.movable_columns, key=lambda c: c.length, reverse=True):
        for possible_position in column.iter_permutations():
            possible_position.is_fixed = True
            permuted_crossword = crossword.copy()
            permuted_crossword.set_column(possible_position)
            if not permuted_crossword.is_invalid():
                yield permuted_crossword
                yield from generate_solutions(permuted_crossword)


def solve(initial_crossword: CrosswordSolution):
    for solution in generate_solutions(initial_crossword):
        print()
        print(solution.pretty_str())
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

    cw = CrosswordSolution.from_string(cross_string)
    print(cw.pretty_str())
    cw.reset()
    print(cw.pretty_str())
    sl = solve(cw)
    print(sl.pretty_str())
