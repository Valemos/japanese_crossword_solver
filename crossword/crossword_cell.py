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
