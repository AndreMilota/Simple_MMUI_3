# manages speech commands

class Command_Buffer:
    def __init__(self):
        self.buffer = []
    def add_command(self, command):
        self.buffer.append(command)

    def get_command(self):
        # append all the commands in the buffer into a string
        command = ""
        for c in self.buffer:
            command += c + " "
        # clear the buffer
        return command

    def clear_buffer(self):
        self.buffer = []

    def undo(self):
        if len(self.buffer) > 0:
            self.buffer.pop()
            return True
        return False # if this happens you may want to undo the application state instead of the command buffer
