# Here are classes that are not used in the test programs

class Message:
    def interpret(self):
        """" [a-zA-Z0-9\s]+ """


class Log:
    def __init__(self, message: Message):
        self.message = message

    def interpret(self):
        print("log:")
        print(self.message)


class ReportSteps:
    @staticmethod
    def interpret(robot):
        print(f"The robot walked {robot.all_steps} steps")
