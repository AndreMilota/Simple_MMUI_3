# this is used to test the two_step_core.py\

from two_step_core import Two_Stage_LLM_Processor
from cross_platform_tool_box import Tool_Box, Tool, Parameter
from primary_prompt_assembler import Primary_Prompt_Assembler
from two_step_core import Two_Stage_LLM_Processor
import json

button_colors = ["red", "green", "blue"]
index_parameter = {"parameter_or_name": "button_index",
                   "description": "The index of the button to change. Buttons are numbered starting from 0 up to n - 1.",
                   "type": "integer"}



def test_1():
    # load the primary tool boxs
    primary_tool_box = Tool_Box()

    def get_button_color(button_index: int) -> (str, bool):
        color = button_colors[button_index]
        out = f"The color of button {button_index} is {color}"
        return out, True

    tool = Tool(get_button_color,
                name = "get_button_color",
                description = "Get the background color of a button.")
    tool.add_required_parameter(**index_parameter)
    primary_tool_box.add_tool(tool)
    primary_prompt_assembler = Primary_Prompt_Assembler(primary_tool_box)

    core = Two_Stage_LLM_Processor([primary_prompt_assembler, primary_prompt_assembler])
    command_1 = "what color is button 2"
    response = core.step(command_1)
    # print the type of response
    print(response)
    pqr1 = core.process_query_response(response)
    print ("pqr1 = ", pqr1)

def main():
    test_1()

if __name__ == "__main__":
    main()