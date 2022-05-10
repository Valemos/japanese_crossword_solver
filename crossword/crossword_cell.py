import enum


class CrosswordCell(enum.Enum):
    EMPTY = ' '
    ACTIVE = '*'

    @classmethod
    def from_bool(cls, value):
        if bool(value):
            return cls.ACTIVE
        else:
            return cls.EMPTY

    def to_int(self):
        return 1 if self is CrosswordCell.ACTIVE else 0
