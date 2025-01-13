# Includes Program, and classes for the program; the grid and the robot

from Statement import Robol
from Enums import *
from Exp import *


class Program:
    def __init__(self, grid, robot):
        self.grid = grid 
        self.robot = robot

    def interpret(self):
        self.robot.interpret()


class Grid:
    def __init__(self, rows: Number, columns: Number):
        # Must evaluate to get int
        self.rows = rows.evaluate()
        self.columns = columns.evaluate()
        self.grid = [[None for column in range(self.columns)]for row in range(self.rows)]
        self.size = (self.columns * self.rows)

    def get_grid(self):
        return self.grid

    def get_size(self):
        return self.size


class Start:
    def __init__(self, column: Number, row: Number):
        self.column = column.evaluate()
        self.row = row.evaluate()

    def interpret(self):
        print(f"Start: ({self.column},{self.row})")


class Robot(Robol):
    def __init__(self, bindings, statements, procdecls, grid, start: Start):
        self.bindings = bindings         # HashMap of Identifiers and their Numbers
        self.statements = statements     # list of statements
        self.procdecls = procdecls       # list of procedure declarations
        self.grid = grid
        self.start = start
        self.stack = []            # Stack for activation records. Regular list
        self.current_column = start.column
        self.current_row = start.row
        self.direction_list = ["east", "south", "west", "north"]
        self.index = 0
        self.facing = self.direction_list[self.index]      # east
        self.all_steps = 0

    def get_recent_steps(self):
        return self.all_steps

    def get_bindings(self):
        return self.bindings

    def get_stack(self):
        return self.stack

    def get_procdecls(self):
        return self.procdecls

    def change_direction(self, direction):
        if direction == Direction.CLOCKWISE:
            # To avoid out-of-bounds-error since north is at the end of the direction_list:
            if self.facing == "north":
                self.facing = "east"
                self.index = 0
            else:
                self.index += 1
                self.facing = self.direction_list[self.index]
        # Counterclockwise:
        else:
            # To avoid out-of-bounds-error:
            if self.facing == "east":
                self.facing = "north"
                self.index = 3
            else:
                self.index -= 1
                self.facing = self.direction_list[self.index]

    # If facing east then walks towards end of columns, if facing south then walks downwards towards start of rows, if facing west
    # then walks towards start of columns, and if facing north then walks upwards towards end of rows.
    def walk(self, exp):
        # east
        if self.facing == self.direction_list[0]:
            self.current_column += exp
        # south
        elif self.facing == self.direction_list[1]:
            self.current_row -= exp
        # west
        elif self.facing == self.direction_list[2]:
            self.current_column -= exp
        # north
        else:
            self.current_row += exp
        self.all_steps += exp          # Steps added to total steps-variable

    # Exception raised if robot's column or row is same/bigger number than the grid, or smaller than 0
    def check_fall(self):
        if(self.current_column < 0 or self.current_column >= self.grid.columns) or (self.current_row < 0
                                                                                    or self.current_row >= self.grid.rows):
            raise IndexError

    def print_position(self):
        print(f"Position: ({self.current_column},{self.current_row})")

    # If IndexError is raised when robot is walking, this gets handled here:
    def interpret(self):
        self.start.interpret()
        try:
            for statement in self.statements:
                statement.interpret(self)
        except IndexError:
            print("The robot fell off the world!")
