# InvalidCommand: Exception when an invalid command is entered
class InvalidCommand(Exception):
    def __init__(self, commandName: str):
        super().__init__(f"Unable to find command by the name '{commandName}'")