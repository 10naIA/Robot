# Test programs for Oblig 1. Written in Python
from Movements import Step
from Robot import *
from Enums import *
from Statement import *
from Exp import *
import sys


def program1():
    grid = Grid(Number(64), Number(64))
    start = Start(Number(23), Number(30))
    bindings = {}
    procdecls = []
    statements = [
        Turn(Direction.CLOCKWISE),
        Turn(Direction.CLOCKWISE),
        Step(Number(15)),
        Turn(Direction.COUNTERCLOCKWISE),
        Step(Number(15)),
        Turn(Direction.COUNTERCLOCKWISE),
        Step(ArithmeticExp(BinaryOp.PLUS, Number(2), Number(3))),
        Turn(Direction.COUNTERCLOCKWISE),
        Step(ArithmeticExp(BinaryOp.PLUS, Number(17), Number(20))),
        Stop()
    ]
    robot = Robot(bindings, statements, procdecls, grid, start)
    program = Program(grid, robot)
    program.interpret()
    # result: (13,52)


# program1()


def program2():
    grid = Grid(Number(64), Number(64))
    start = Start(Number(23), Number(6))
    bindings = {Identifier("i"): Number(5), Identifier("j"): Number(3)}
    statements = [
        Turn(Direction.COUNTERCLOCKWISE),
        Step(ArithmeticExp(BinaryOp.MULTIPLY, Number(3), Identifier("i"))),
        Turn(Direction.CLOCKWISE),
        Step(Number(15)),
        Turn(Direction.CLOCKWISE),
        Step(ArithmeticExp(BinaryOp.MINUS, ArithmeticExp(BinaryOp.MINUS, Number(12), Identifier("i")), Identifier("j"))),
        Turn(Direction.CLOCKWISE),
        Step(ArithmeticExp(BinaryOp.PLUS, ArithmeticExp(
            BinaryOp.PLUS, ArithmeticExp(BinaryOp.MULTIPLY, Number(2), Identifier("i")),
            ArithmeticExp(BinaryOp.MULTIPLY, Number(3), Identifier("j"))), Number(1))),
        Stop()
    ]
    procdecls = []
    robot = Robot(bindings, statements, procdecls, grid, start)

    program = Program(grid, robot)
    program.interpret()
    # Result: (18,17)


# program2()


def program3():
    grid = Grid(Number(64), Number(64))
    start = Start(Number(23), Number(6))
    bindings = {Identifier("i"): Number(5), Identifier("j"): Number(4)}
    statements = [
        Turn(Direction.COUNTERCLOCKWISE),
        Step(ArithmeticExp(BinaryOp.MULTIPLY, Number(3), Identifier("i"))),
        Turn(Direction.COUNTERCLOCKWISE),
        Step(Number(15)),
        Turn(Direction.CLOCKWISE),
        Turn(Direction.CLOCKWISE),
        Step(Number(4)),
        Turn(Direction.CLOCKWISE),
        Loop(ArithmeticExp(BinaryOp.GREATER, Identifier("j"), Number(1)),
             [Step(Identifier("j")), Assignment(Identifier("j"), "--")]),
        Stop()
    ]

    procdecls = []
    robot = Robot(bindings, statements, procdecls, grid, start)

    program = Program(grid, robot)
    program.interpret()
    # Resultat: (12,12)


# program3()


def program4():
    grid = Grid(Number(64), Number(64))
    start = Start(Number(1), Number(1))
    bindings = {Identifier("i"): Number(8)}
    statements = [
        Loop(ArithmeticExp(BinaryOp.LESS, Identifier("i"), Number(100)), [Step(Identifier("i"))]),
        Stop()
    ]

    procdecls = []
    robot = Robot(bindings, statements, procdecls, grid, start)
    program = Program(grid, robot)
    program.interpret()
    # Result: Exception: Robot falls over edge


# program4()


def program5():
    grid = Grid(Number(64), Number(64))
    bindings = {Identifier("x"): Number(1), Identifier("y"): Number(5)}

    procdecls = [
        Procedure(Identifier("p1"), [Step(Identifier("a")), Turn(Direction.CLOCKWISE), Step(Identifier("b"))],
                  {Identifier("a"): None, Identifier("b"): None})
    ]
    start = Start(Number(23), Number(30))
    statements = [
        Call(Identifier("p1"), Identifier("x"), Identifier("y")),
        Turn(Direction.CLOCKWISE),
        Call(Identifier("p1"), Identifier("y"), Identifier("x")),
        Stop()
    ]

    robot = Robot(bindings, statements, procdecls, grid, start)
    program = Program(grid, robot)
    program.interpret()
    # Result: 19,26


# program5()


def program6():
    grid = Grid(Number(64), Number(64))
    bindings = {Identifier("x"): Number(3), Identifier("y"): Number(3)}
    procdecls = [
        Procedure(Identifier("p1"), [Step(Identifier("a")), Step(Identifier("b")), Assignment(Identifier("a"), "--")],
                  {Identifier("a"): None, Identifier("b"): None}),
        Procedure(Identifier("p2"), [Step(Identifier("a")), Step(Identifier("b")), Assignment(Identifier("b"), "--")],
                  {Identifier("a"): None, Identifier("b"): None})
    ]

    start = Start(Number(23), Number(30))
    statements = [
        Call(Identifier("p1"), Identifier("x"), Identifier("y")),
        Call(Identifier("p2"), Identifier("x"), Identifier("y")),
        Step(Identifier("x")),
        Step(Identifier("y")),
        Stop()
    ]
    robot = Robot(bindings, statements, procdecls, grid, start)
    program = Program(grid, robot)
    program.interpret()
    # Result: 41,30


# program6()


def oblig1(n):
    if n == "1":
        program1()
    elif n == "2":
        program2()
    elif n == "3":
        program3()
    elif n == "4":
        program4()
    elif n == "5":
        program5()
    elif n == "6":
        program6()
    elif n == "all":
        program1()
        print("\n")
        program2()
        print("\n")
        program3()
        print("\n")
        program4()
        print("\n")
        program5()
        print("\n")
        program6()
        print("\n")
    else:
        print("USAGE: python Robot.py 1|2|3|4|5|6|7|all")


# Starts running when file is called from command line. Needs one argument
if __name__ == "__main__":
    oblig1(sys.argv[1])
