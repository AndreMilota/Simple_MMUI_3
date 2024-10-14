# secondary_prompt_assembler.py
# Assembles The Prompt for the second call of the llm when information is available and actions should be taken

from typing import List, Any, Union
from gesture_manager import Gesture_Manager

class Secondary_Prompt_Assembler:
    def __init__(self, tool_box, number_of_buttons = 3):
        self.tool_box = tool_box
        self.number_of_buttons = number_of_buttons

        self.MMUI_instructions = "You are a helpful assistant that controls a multimodal user interface. You will be given the text " \
        "of what the user said and a description of the objects they indicated using gestures." \
        "\n First, combine these inputs, using the gesture descriptions to resolve pronouns and ambiguous references in the text. "

        self.SUI_instructions = """"You are a helpful assistant that controls a speech user interface. You will be given the text of what the user said. """

        self.has_information = "We know that: "

        self.end_instructions = """You must either:
        1) answer the users question.
        2) make the necessary function calls to change the application in the way the user requested. """

        self.end_instructions += f'There are a total of {number_of_buttons} buttons with indexes starting at 0. '

        self.end_instructions += 'When the user says they want to change the color of button 1 they mean the button with index 1, not index 0 or 2. '

    def compute_prompt(self, command: str, gesture: Union[Gesture_Manager, str], response :str = None) -> list:
        # see if the gesture_manager is an instance of the Gesture_Manager class
        c_and_g = f"{command}"

        if isinstance(gesture, Gesture_Manager):
            gesture_description = gesture.get_description()
        else:
            gesture_description = gesture

        if not gesture_description:
            instructions = self.SUI_instructions
        else:
            instructions = self.MMUI_instructions
            c_and_g += ". " + gesture_description

        if response:
            instructions += self.has_information + response

        instructions += self.end_instructions

        prompt = [{
            "role": "assistant",
            "content": instructions }]
        messages = [{"role": "user", "content": c_and_g}]

        prompt += messages
        return prompt