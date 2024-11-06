# SQL_prompt_assembler.py

from typing import List, Any, Union
from gesture_manager import Gesture_Manager

class Primary_Prompt_Assembler:
    def __init__(self, db):
        self.database = db
        self.number_of_buttons = db.get_number_of_buttons()

        self.MMUI_instructions = """"You are doing the first phase of processing for a multimodal user interface. You will be given the text of what the 
                user said and a description of the objects they indicated using gestures. First, combine these using the gesture descriptions 
                to resolve pronouns and ambiguous references in the text. Then """

        self.SUI_instructions = """"You are doing the first phase of processing for a speech user interface. You will be given the text 
                of what the user said to resolve pronouns and ambiguous references in the text. """

        self.general_instructions = """You will have to handle one of three situations as follows:
                1. The user asks a question for which you already have the information to answer. In this case, print the answer. For example, 
                the user might ask: "What color are carrots typically?" You should respond: "Orange."
                2. The user will ask you to change the state of the application. You will do this by altering and possibly querying the database 
                table containing the states of the buttons using SQL that you will need to return. 
                3. The user will ask a question about the interface and you will write a SQL query to 
                get the needed information. This information will be given to an LLM with a different prompt to make the appropriate response.
                """

        self.general_instructions += """If you generate SQL, please wrap it in `<SQL>` and `</SQL>` tags. For example:
            <SQL>
            If you generate SQL, please wrap it in `<SQL>` and `</SQL>` tags. For example:
            <SQL>
            """

    def compute_prompt(self, command: str, gesture: Union[Gesture_Manager, str], response: str = None) -> list:
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