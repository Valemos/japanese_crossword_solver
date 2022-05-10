import numpy as np

import parse_crossword
from crossword.cell_block import CellBlock
from crossword.block_direction import Direction
from crossword.cell_block_set import CellBlockSet
from crossword.crossword_hints import CrosswordHintsHorizontal, CrosswordHintsVertical
from crossword.crossword_solution import CrosswordSolution


def test_crossword_print():
    crossword = CrosswordSolution(np.asarray([
                                      [1, 1, 0],
                                      [0, 1, 0],
                                      [0, 1, 1],
                                  ]))
    crossword._h_hints = CrosswordHintsHorizontal([[1, 10, 1], [2, 2], [1, 2, 3, 4]])
    crossword._v_hints = CrosswordHintsVertical([[3, 3], [4, 40, 4], [5, 5]])

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

    cross = CrosswordSolution.from_string(cross_string)
    print()
    print(cross.pretty_str())
    assert cross._h_hints.hints == [[1, 1], [1, 1], [1, 1], [4]]
    assert cross._v_hints.hints == [[1], [2, 1], [1], [1], [2, 1], [1]]
    assert not cross.is_invalid()
    assert cross.is_solved()
    cross._solution[0, 0] = 1
    assert cross.is_invalid()


def test_cell_parameters():
    assert CellBlock(1, 1).last_position == 1
    assert CellBlock(1, 0).last_position == 0
    assert CellBlock(3, 0).last_position == 2
    assert CellBlock(3, 2).last_position == 4


def test_cell_block_set():
    block_set = CellBlockSet(0, Direction.VERTICAL, [1, 2, 1, 3])
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

    column = CellBlockSet(0, Direction.VERTICAL, [1, 2, 1])
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


def test_copy():
    sample_link = "15x15:2.1.1.1.3/2.1.2/2.1.1.2/4.1.6/4.9/1.5.2/3.1/5/2.5/2.3.6/1.2.8" \
                  "/2.4.2/3.3/3.3/3/4.3/5.1.1/3/2.1/3.1.3/1.4/1.4.3/5.4/1.10/3.5/2.2.3" \
                  "/5.3/1.2.3.3/4.6/5.5"
    cw = parse_crossword.from_link(sample_link)

    assert cw == cw.copy()


def test_iterate_positions():
    column = CellBlockSet(0, Direction.VERTICAL, [1, 2, 1])
    assert list(column.iter_positions()) == [0, 2, 3, 5]
