# File with Enum classes for binary operations and directions.

from enum import Enum
import operator


class BinaryOp(Enum):
    PLUS = operator.add
    MINUS = operator.sub
    MULTIPLY = operator.mul
    LESS = operator.lt          # <
    GREATER = operator.gt       # >
    EQUAL = operator.eq


class Direction(Enum):
    CLOCKWISE = "clockwise"
    COUNTERCLOCKWISE = "counterclockwise"
