from dataclasses import dataclass


@dataclass
class CellBlock:
    position: int = 0
    length: int = 1

    def __hash__(self):
        return abs(hash((self.position, self.length)))

    def __eq__(self, other):
        return self.position == other.position and \
                self.length == other.length

    @property
    def last_position(self):
        return self.position + self.length - 1

    def contains_position(self, position):
        return self.position <= position <= self.position + self.length
