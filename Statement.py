# Statement superclass and its subclasses; Stop, Assignment, Loop and Call

from Movements import Turn
from Exp import ArithmeticExp, Number
from ProcedureStack import *
from abc import ABC, abstractmethod
import copy


class Robol:
    def interpret(self):
        pass


class Statement(Robol, ABC):
    @abstractmethod
    def interpret(self, *args):
        pass


class Stop(Statement):
    def interpret(self, robot, activation_record=None):
        # Want output on same line, use end="" because robot.print_position() also prints, and can't be inside this print
        print("Stop. ", end="")
        robot.print_position()


# Ex: Identifier(i) > Number(5)
class Assignment(Statement):
    def __init__(self, identifier, op):
        self.identifier = identifier    # Identifier-object
        self.op = op
        self.number = 0

    def update_number(self, number):
        self.number = number

    def get_identifier(self):
        return self.identifier

    def update_identifier(self, new_identifier):
        self.identifier = new_identifier

    def interpret(self, robot):
        if self.op == "++":
            self.number += 1
        else:
            self.number -= 1
        return self.number


class Loop(Statement):
    def __init__(self, boolean_exp: ArithmeticExp, statements):
        self.boolean_exp = boolean_exp
        self.statements = statements      # list

    def get_identifier(self):
        return self.boolean_exp.get_identifier()

    def update_identifier(self, new_identifier):
        self.boolean_exp.update_identifier(new_identifier)

    def interpret(self, robot, activation_record=None):
        bindings = robot.get_bindings()
        while self.boolean_exp.evaluate(bindings) != 0:
            for statement in self.statements:
                if not (isinstance(statement, Turn) or isinstance(statement, Stop) or isinstance(statement, Call)):
                    if activation_record is not None:
                        # If f.ex statement is Step or Assignment, it needs to get and update the value of either a or b
                        value = activation_record.get_local_variable(statement.get_identifier())
                        statement.update_identifier(value)
                    if isinstance(statement, Assignment):
                        # Search in bindings to get correct key and update it's number
                        for key in bindings.keys():
                            if key == statement.get_identifier():
                                statement.update_number(bindings[key].evaluate())
                                # update value in local bindings-map, so if f.ex i = 5 and then i-- gives i --> 4:
                                bindings[key] = Number(statement.interpret(robot))
                                self.boolean_exp.update_identifier(bindings[key].evaluate())
                    else:
                        statement.interpret(robot)
                else:
                    statement.interpret(robot)


# Used for structure when procedures are called
class Call(Statement):
    # *args for varying number of arguments
    def __init__(self, identifier, *args):
        self.identifier = identifier
        self.args = args

    def get_identifier(self):
        return self.identifier

    def get_args(self):
        return self.args

    def interpret(self, robot):
        for proc in robot.get_procdecls():
            # To find correct procedure-name in proc_decls, we compare the identifier to the one in the statement
            if proc.get_identifier() == self.identifier:
                # Make local copy of the procedure statements so changes only happen locally
                proc_body_copy = copy.deepcopy(proc.get_proc_body())
                # Use deepcopy to get copy of local variables-HashMap
                local_variables = copy.deepcopy(proc.get_proc_params())
                if len(robot.get_stack()) != 0:
                    outer_activation_record = robot.get_stack()[-1]
                    access_link = outer_activation_record.get_global_variables()
                    activation_record = ActivationRecord(access_link, local_variables)
                else:
                    activation_record = ActivationRecord(self.args, local_variables)
                activation_record.set_local_variables()
                robot.get_stack().insert(0, activation_record)  # push to stack
                for local_statement in proc_body_copy:
                    if not (isinstance(local_statement, Stop) or isinstance(local_statement, Turn)):
                        local_variable = local_statement.get_identifier()
                        value = activation_record.get_local_variable(local_variable)
                        local_statement.update_identifier(value)
                    # Because local_statement might be loop, activation_record is an argument (is ignored in other
                    # interpret-methods)
                    local_statement.interpret(robot)
        robot.get_stack().pop(0)  # pop from stack