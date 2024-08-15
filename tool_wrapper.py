# This class is used to associate a function pointer with a tool, along with any additional information we want to
# include, such as examples or instructions that will ultimately be part of the prompt. It can also potentially be used
# to connect control information so that if a function is called, the LLM will not be recalled to process its results.
# Additionally,this class can handle converting arguments for the LLM.
import inspect
class Tool_Wrapper:
    def __init__(self, function, examples, instructions):
        self.function = function
        self.examples = examples
        if not instructions:
            self.instructions = inspect.getdoc(function)
        else:
            self.instructions = instructions

    def __str__(self):
        return f"Function: {self.function}, Examples: {self.examples}, Instructions: {self.instructions}"

    def __call__(self, dictinary_args):
        return self.function(**dictinary_args)
