# This file is used to generate examples.  one specifies a series of actions and responses and then it can generate the
# appropriate examples for both the first and second pass.

class Example_Generator:
    def __init__(self, tool_boxes, prompt_assemblers):
        self.tool_boxes = tool_boxes
        self.prompt_assemblers = prompt_assemblers