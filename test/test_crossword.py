import numpy as np

import parse_crossword
from crossword.cell_block import CellBlock
from crossword.block_direction import BlockDirection
from crossword.cell_block_set import CellBlockSet
from crossword.crossword_hints import CrosswordHints
from crossword.crossword_solution import CrosswordSolution


def test_crossword_print():

    hints = CrosswordHints([[1, 10, 1], [2, 2], [1, 2, 3, 4]],
                           [[3, 3], [4, 40, 4], [5, 5]])
    crossword = CrosswordSolution(hints,
                                  np.asarray([
                                      [1, 1, 0],
                                      [0, 1, 0],
                                      [0, 1, 1],
                                  ]))
    print()
    print(crossword.pretty_str())


def test_create_from_link():
    sample_link = "15x15:2.1.1.1.3/2.1.2/2.1.1.2/4.1.6/4.9/1.5.2/3.1/5/2.5/2.3.6/1.2.8" \
                  "/2.4.2/3.3/3.3/3/4.3/5.1.1/3/2.1/3.1.3/1.4/1.4.3/5.4/1.10/3.5/2.2.3" \
                  "/5.3/1.2.3.3/4.6/5.5"

    print()
    print(parse_crossword.from_link(sample_link).pretty_str())


def test_create_from_string():
    cross_string = " *  * \n" \
                   " *  * \n" \
                   "*    *\n" \
                   " **** \n"

    cross = parse_crossword.create_from_string(cross_string)
    print()
    print(cross.pretty_str())


def test_cell_parameters():
    assert CellBlock(1, 1).last_position == 1
    assert CellBlock(1, 0).last_position == 0
    assert CellBlock(3, 0).last_position == 2
    assert CellBlock(3, 2).last_position == 4


def test_cell_block_set():
    block_set = CellBlockSet(0, BlockDirection.VERTICAL, [1, 2, 1, 3])
    assert block_set.length == 10

    assert block_set.blocks[0].position == 0
    assert block_set.blocks[0].last_position == 0
    assert block_set.blocks[1].position == 2
    assert block_set.blocks[1].last_position == 3
    assert block_set.blocks[2].position == 5
    assert block_set.blocks[2].last_position == 5
    assert block_set.blocks[3].position == 7
    assert block_set.blocks[3].last_position == 9


def test_cell_block_permutations():
    expected = {
        "0-00-0--",
        "0-00--0-",
        "0-00---0",
        "0--00-0-",
        "0--00--0",
        "-0-00-0-",
        "-0-00--0",
        "0---00-0",
        "-0--00-0",
        "--0-00-0",
        "0--00-0-",
    }

    column = CellBlockSet(0, BlockDirection.VERTICAL, [1, 2, 1])
    column.set_max_length(8)

    ls = list(map(str, column.get_permutations()))
    unique = set(ls)

    counts = {el: 0 for el in unique}
    for el in ls:
        counts[el] += 1

    print()
    for key in sorted(counts, key=lambda kw: kw[0]):
        print(f"{key}\t= {counts[key]}")

    assert expected == unique
