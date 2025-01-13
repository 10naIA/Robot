# Classes for the robot's movements; Turn and Step

class Turn:
    def __init__(self, direction):
        self.direction = direction

    # Might be called from a statement that might also be a loop (which needs an activation_record), therefore interpret-method
    # have placeholder for activation_record, but it's not used here
    def interpret(self, robot, activation_record=None):
        robot.change_direction(self.direction)


class Step:
    def __init__(self, number):
        self.number = number          # Type: Either Number or Identifier

    def update_identifier(self, new_number):
        self.number = new_number

    def get_identifier(self):
        return self.number

    # Evaluates the number-variable so it returns an int, so the robot can walk. Also checks if the robot falls over the edge
    def interpret(self, robot, activation_record=None):
        bindings = robot.get_bindings()
        robot.walk(self.number.evaluate(bindings))
        robot.check_fall()
        robot.print_position()
