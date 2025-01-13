# Exp superclass and its subclasses; Number, BoolExp, ArithmeticExp and Identifier

from abc import ABC, abstractmethod
from Enums import BinaryOp


class Exp(ABC):
    @abstractmethod
    def evaluate(self, *args):
        pass


class Number(Exp):
    def __init__(self, number):
        self.number = number

    def evaluate(self, bindings=None):
        # In case we have a Number(Number(1)) which needs to be evaluated twice
        if isinstance(self.number, Number):
            self.number = self.number.evaluate()
        return self.number


class BoolExp(Exp, ABC):
    def __init__(self, expression):
        self.expression = expression

    @abstractmethod
    def evaluate(self, bindings: None):
        pass


class ArithmeticExp(Exp):
    def __init__(self, binary_op: BinaryOp, left, right):
        self.operation = binary_op
        self.left = left
        self.right = right

    def get_identifier(self):
        return self.left

    def update_identifier(self, new_left):
        self.left = new_left

    def evaluate(self, bindings):
        # Need right and left to be int for them to be calculated with the operation.value.
        if not isinstance(self.right, int):
            self.right = self.right.evaluate(bindings)
        if not isinstance(self.left, int):
            self.left = self.left.evaluate(bindings)
        if self.operation not in [BinaryOp.GREATER, BinaryOp.LESS, BinaryOp.EQUAL]:
            return Number(self.operation.value(self.left, self.right)).evaluate()
        else:
            # If boolean expression is false, it returns 0
            if not self.operation.value(self.left, self.right):
                return 0
            else:
                return 1


class Identifier(Exp):
    def __init__(self, string):
        self.string = string

    def get_identifier(self):
        return self.string

    def update_identifier(self, new_string):
        self.string = new_string

    # Used to find correct letter in the bindings-HashMap
    def __eq__(self, other):
        return self.string == other.string and isinstance(other, Identifier)

    # Needed to compare two objects, like two Identifier objects in a HashMap
    def __hash__(self):
        return hash(self.string)

    def evaluate(self, bindings):
        for key in bindings.keys():
            if key.string == self.string:
                value = bindings[key]
                return value.evaluate()        # Returns int. Evaluate because value in bindings is Number, and we need int
