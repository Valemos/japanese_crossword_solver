import parse_crossword
from crossword.crossword_solution import CrosswordSolution


def generate_solutions(crossword: CrosswordSolution):
    yield crossword
    for column in sorted(crossword.movable_columns, key=lambda c: c.length, reverse=True):
        for possible_position in column.get_permutations():
            possible_position.is_fixed = True
            permuted_crossword = crossword.copy()
            permuted_crossword.set_column(possible_position)
            print(f"change col: {possible_position.position}", end='\r\n')
            if not permuted_crossword.is_invalid():
                yield permuted_crossword
            yield from generate_solutions(permuted_crossword)


# takes too much time
def solve_bruteforce(crossword: CrosswordSolution):
    for solution in generate_solutions(crossword):
        # print()
        # print(solution.pretty_str())
        if solution.is_solved():
            return solution

    raise RuntimeError("crossword has no solutions")


def solve_clever(crossword: CrosswordSolution):
    for column in sorted(crossword.movable_columns, key=lambda c: c.length, reverse=True):
        modified_crossword = crossword.copy()

        try:
            return solve_clever(modified_crossword)
        except RuntimeError:
            pass


if __name__ == '__main__':
    cross_simple = " *  * \n" \
                   " *  * \n" \
                   "*    *\n" \
                   " **** \n"

    cw = CrosswordSolution.from_string(cross_simple)
    print("Before")
    cw = cw.reset()
    print(cw.pretty_str())
    sl = solve_bruteforce(cw)
    print("Solved!")
    print(sl.pretty_str())
    exit(0)

    cw_link = "15x15:2.1.1.1.3/2.1.2/2.1.1.2/4.1.6/4.9/1.5.2/3.1/5/2.5/2.3.6/1.2.8" \
                  "/2.4.2/3.3/3.3/3/4.3/5.1.1/3/2.1/3.1.3/1.4/1.4.3/5.4/1.10/3.5/2.2.3" \
                  "/5.3/1.2.3.3/4.6/5.5"

    cw = parse_crossword.from_link(cw_link)
    print("Before")
    print(cw.pretty_str())
    sl = solve_bruteforce(cw)
    print("Solved!")
    print(sl.pretty_str())

