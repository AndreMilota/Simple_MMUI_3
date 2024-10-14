# primary_prompt_assembler

from typing import List, Any, Union
from gesture_manager import Gesture_Manager
from typing import Any

class Primary_Prompt_Assembler:
    def __init__(self, tool_box, number_of_buttons = 3):
        self.tool_box = tool_box
        self.number_of_buttons = number_of_buttons

        self.MMUI_instructions = """"You are doing the first phase of processing for a multimodal user interface. You will be given the text of what the 
        user said and a description of the objects they indicated using gestures. First, combine these using the gesture descriptions 
        to resolve pronouns and ambiguous references in the text. Then """

        self.SUI_instructions = """"You are doing the first phase of processing for a speech user interface. You will be given the text 
        of what the user said to resolve pronouns and ambiguous references in the text. """

        self.general_instructions = """You will have to handle one of three situations as follows:
        1.	The user asks a question for which you already have the information to answer. In this case, print the answer. For example, 
        the user might ask: "What color are carrots typically?" You should respond: "Orange."
        2.	The user gives a command. In this case, you should return nothing. For example, the user might say: "Make this blue," and point 
        to button number one. In this case, don't do anything.
        3.	The user asks a question or gives a command that requires you to get information about the state of the system. For example, 
        the user might say: "Make button one and two the same color as button zero." In this case, you need to call the function to get 
        the color of button zero. """

        self.general_instructions += 'If you are asked some general question about all the buttons in aggregate such as what is the most common color or which button is colored differently from the others then you will need to  make a query to find out the color of each of the buttons in turn. '

        #self.general_instructions += 'There are a total of' + number_of_buttons + 'buttons with indexes starting at 0. '
        self.general_instructions += f'There are a total of {number_of_buttons} buttons with indexes starting at 0. '

    def compute_prompt(self, command: str, gesture: Union[Gesture_Manager, str], response :str = None) -> list:
        assert (response is None), "This function does not use the response parameter"

        # see if the gesture_manager is an instance of the Gesture_Manager class
        if isinstance(gesture, Gesture_Manager):
            gesture_description = gesture.get_description()
        else:
            gesture_description = gesture

        if gesture_description is None:
            instructions = self.SUI_instructions + self.general_instructions
            prompt = [{
                "role": "assistant",
                "content": instructions }]
            messages = [{"role": "user", "content": command}]
        else:
            instructions = self.MMUI_instructions + self.general_instructions
            prompt = [{
                "role": "assistant",
                "content": instructions }]
            c_and_g = f"{command}"
            c_and_g += ". " + gesture_description

            messages = [{"role": "user", "content": c_and_g}]

        prompt += messages
        return prompt