# This file is used to generate examples.  one specifies a series of actions and responses and then it can generate the
# appropriate examples for both the first and second pass.

class Example_Generator:
    def __init__(self, command, prompt_assemblers, platforms, gestures = []):
        self.command = command
        self.gestures = gestures
        self.prompt_assemblers = prompt_assemblers
        # see if platform is a string or list of strings
        if isinstance(platforms, list):
            self.platforms = platforms
        else:
            self.platforms = [platforms, platforms]
        self.primary_calls = []
        self.secondary_calls = []

    def add_primary_call(self, function_name, args, result):
        self.primary_calls.append((function_name, args, result))

    def add_secondary_call(self, function_name, args, result):
        self.secondary_calls.append((function_name, args, result))

    def generate_secondary_examples(self):
