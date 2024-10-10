# This agent is updated to use the more general toolbox class

from Open_AI_Toolbox import Tool_Box
from Open_AI_Toolbox import Tool
from typing import Tuple
import agent_core as AC
import GUI_4 as GUI
import GUI_stub_wrapper as GUI_Offline
import offline_tests_2 as OT
from agent_core import Agent_Core
from gesture_manager import Gesture_Manager

from model_manager import identify_model

def load_tools(gui, model) -> Tool_Box:
    out = Tool_Box()

    service = identify_model(model)
    index_parameter = {"name": "button_index",
                      "description": "The index of the button to change. Buttons are numbered starting from 0 up to n - 1.",
                      "type": "integer"}


    # add the tools here
    #def set_button_color(button_index: int, color_name: str) -> str
    # returns a string and a bool to indicate that more actions are needed
    def set_button_color(button_index: int, color_name: str) -> Tuple[str, bool]:
        """Set the background color of a button."""
        gui.set_button_color(button_index, color_name)
        out = f"Set button {button_index} to {color_name}"
        return out, False

    tool = Tool(set_button_color, name = "set_button_color",
                description = "Set the background color of a button.",
                service = service)
    tool.add_required_parameter(**index_parameter)
    tool.add_required_parameter("color_name", "The name of the color to change the button to.", "string")
    out.add_tool(tool)

    # ------------------------------------------------------------------------------
    # add the get_button_color tool

    def get_button_color(button_index: int) -> Tuple[str, bool]:
        """Get the background color of a button."""
        out = gui.get_button_color(button_index)
        return out, True

    tool = Tool(get_button_color, name = "get_button_color",
                description = "Get the background color of a button.",
                service = service)
    tool.add_required_parameter(**index_parameter)
    out.add_tool(tool)

    return out;