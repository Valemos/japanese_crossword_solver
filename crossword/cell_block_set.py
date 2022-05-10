from copy import deepcopy
import hashlib

from crossword.cell_block import CellBlock
from crossword.block_direction import BlockDirection


class CellBlockSet:
    """block set maintains at least one empty cell between all blocks"""

    def __init__(self, position, direction, lengths: list):
        self._blocks = [CellBlock(position, lengths[0])]
        for length in lengths[1:]:
            new_cell_start = self._blocks[-1].last_position + 2
            new_cell = CellBlock(new_cell_start, length)
            self._blocks.append(new_cell)

        self._max_length = float("inf")
        self.position = position
        self.direction = direction

    def __str__(self):
        gaps = [self._blocks[0].position]
        for b1, b2 in zip(self._blocks, self._blocks[1:]):
            gaps.append((b2.position - b1.last_position - 1))
        gaps = list('-' * ln for ln in gaps)
        if self._max_length != float("inf"):
            gaps.append('-' * (self._max_length - self.length))
        else:
            gaps.append('')

        block_strings = list(map(lambda b: '0' * b.length, self._blocks))

        result = gaps.pop(0)
        for b_string, gap in zip(block_strings, gaps):
            result += b_string + gap

        return result

    def __hash__(self):
        m = hashlib.md5()
        for block in self._blocks:
            m.update(block.position.to_bytes(8, byteorder='big'))
            m.update(block.last_position.to_bytes(8, byteorder='big'))
        return int.from_bytes(m.digest(), byteorder='big')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.blocks == other.blocks and \
                    self.position == other.position and \
                    self.direction == other.direction

    def set_max_length(self, length):
        self._max_length = length

    @property
    def blocks(self):
        return self._blocks

    @property
    def length(self):
        if len(self._blocks) > 0:
            return self._blocks[-1].last_position + 1
        else:
            return 0

    def contains_point(self, col, row):
        if self.direction == BlockDirection.VERTICAL:
            pos = col
        else:
            pos = row
        return any(block.contains_position(pos) for block in self._blocks)

    def get_permutations(self):
        return self.iter_permutations()

    def iter_permutations(self, fixed_blocks=None):
        if fixed_blocks is None:
            block_lengths = list(map(lambda b: b.length, self._blocks))
            permutation = CellBlockSet(self.position,
                                       self.direction,
                                       block_lengths)
            permutation.set_max_length(self._max_length)
            fixed_blocks = []
        else:
            permutation = deepcopy(self)

        yield permutation

        sweep_blocks = list(range(len(self.blocks) - 1, -1, -1))
        for block_i in fixed_blocks:
            if block_i in sweep_blocks:
                sweep_blocks.remove(block_i)

        for block_i in sweep_blocks:
            while permutation.move_block(block_i):
                yield from permutation.iter_permutations(fixed_blocks + [block_i])

    def move_block(self, block_index):
        """
        moves block by one cell in its direction
        returns False if move invalid and reverts move
        """
        moved_block = self._blocks[block_index]
        moved_block.position += 1

        if block_index < len(self._blocks) - 1:  # block not the last
            collided_block = self._blocks[block_index + 1]
            # blocks collided and move invalid
            if moved_block.last_position == collided_block.position - 1:
                moved_block.position -= 1
                return False
        elif moved_block.last_position >= self._max_length:
            moved_block.position -= 1
            return False

        return True
