# This class contains functions for assembling prompts.
# we may want to add history to this class or a class it uses or wraps it

defalut_prompt_core = """You are a multimodal agent for controlling a simple app.
You will be given the text of the commands the user issues and if they make any gestures you will be given a description of them.
The application you are controlling has {number_of_buttons} buttons.
You can set there by calling the function called set_button_color.
It takes two arguments, the index of the button and the color you want to set it to.
it will return something like 'Set button 1 to red'.
The user may also ask a question that does not entail making a function call.
When asked a question answer with a brief response unless the user asks for you to provide longer responses."""

class Prompt_Assembler:
    def __init__(self, tool_box, prompt_core = None):
        self.tool_box = tool_box
        if not prompt_core:
            self.prompt_core = defalut_prompt_core
        else:
            self.prompt_core = prompt_core
    def compute_prompt(self, command :str, gestures :str) -> list:
        tool_examples = self.tool_box.get_tool_examples(command)
        prompt = self.prompt_core + tool_examples
        # TODO add history here
        c_and_g = f"{command} " # we want to make a copy of the command
        if gestures:
            c_and_g += gestures
        messages =[{"role": "user", "content": c_and_g}]
        prompt += messages
        return prompt
