# This module connects the agent core with the application and starts everything running.

from tool_box import Tool_Box

import agent_core as AC
import GUI_4 as GUI
import offline_tests_2 as OT
from agent_core import Agent_Core
def load_tools(gui) -> Tool_Box:

    out = Tool_Box()
    def set_button_color(button_index: int, new_color: str) -> str:
        """Set the background color of a button."""
        gui.set_button_color(button_index, new_color)
        out = f"Set button {button_index} to {new_color}"
        return out

    # we could use something to make this easier
    example = [
        # give an example of a command
        {
            "role": "user",
            "content": "Make this red. Button 1 was indicated"
        },
        {
            "role": "assistant",
            'tool_calls': [
                {
                    'id': 'call_ywm8',
                    'function': {
                        'name': 'set_button_color',
                        'arguments': '{"button_index": 1, "color_name": "red"}'
                    },
                    'type': 'function'
                }
            ]
        }
    ]

    description = "Sets a button to a given color"
    parameters = {
        "type": "object",
        "properties": {
            "button_index": {
                "type": "integer",
                "description": "The index of the button to change the color of. "
                               "Buttons are numbered starting from 0 up to n - 1.",
            },
            "color_name": {
                "type": "string",
                "description": "The name of the color to change the button to",
            },
        },
        "required": ["button_index", "color_name"],
    }

    out.add_tool(tool=set_button_color,

    return out

class Agent(Agent_Core):
    def __init__(self, gui):
        self.gui = gui
        self.tool_box = load_tools(gui)
        # init the base class
        super().__init__(self.tool_box)
        # link the GUI to the agent
        gui.set_run_callback(self.take_action)

    def get_gui(self):
        return self.gui

    def get_tool_box(self):
        return self.tool_box

    def get_prompt_assembler(self):
        return self.prompt_assembler

    def reset(self):
        self.gui.reset()

def main():
    # for off line testing
    gui = OT.GUIOffline()
    # load the toolbox



