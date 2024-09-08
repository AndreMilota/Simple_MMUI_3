# This class contains functions for assembling prompts.
# we may want to add history to this class or a class it uses or wraps it

import json
from typing import Any


defalut_primary_instructions = """You are a multimodal agent for controlling a simple app.
You will be given the text of the commands the user issues and if they make any gestures you will be given a description of them.
You should look at the gesture descriptions to resolve pronouns in the text of the commands.
For instance if the user say: 'make this the color of this' and makes 2 gestures you should look at what buttons they pointed to, to decide which object to copy the color from and which to apply it to. 
The application you are controlling has {number_of_buttons} buttons.
You can set it by calling the function called set_button_color.
It takes two arguments, the index of the button and the name of the color you want to set it to.
The color must be specified as one of the standard x11 colors or RGB hex.
it will return something like 'Set button 1 to red'.
You can read the color of a button by calling the function get_button_color.
It takes one argument, the index of the button you want to read.
The user may also ask a question that does not entail making a function call.
When asked a question answer with a brief response unless the user asks for you to provide longer responses."""

from gesture_manager import Gesture_Manager

def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))

class Prompt_Assembler:
    def __init__(self, tool_box, number_of_buttons = 3, primary_instructions = None):
        self.tool_box = tool_box
        if not primary_instructions:
            self.primary_instructions = defalut_primary_instructions
            # put in the number of buttons
            self.primary_instructions = self.primary_instructions.format(number_of_buttons=number_of_buttons)
            print("self.primary_instructions", self.primary_instructions)
        else:
            self.primary_instructions = primary_instructions
    def compute_prompt(self, command :str, gesture_manager :Gesture_Manager) -> list:
        prompt = [{
            "role": "assistant",
            "content": self.primary_instructions
        }]
        # tool_examples = self.tool_box.get_tool_examples(command)
        #
        # print("tool_examples", tool_examples)
        # pretty_print(tool_examples)
        #
        # prompt += tool_examples

        print("prompt", prompt)
        pretty_print(prompt)

        # TODO add history here
        c_and_g = f"{command} " # we want to make a copy of the command
        gesture_description = gesture_manager.get_description()
        if gesture_description:
            c_and_g += ". " + gesture_description

        messages =[{"role": "user", "content": c_and_g}]

        print("messages", messages)
        pretty_print(messages)

        prompt += messages

        print("prompt", prompt)
        pretty_print(prompt)

        return prompt