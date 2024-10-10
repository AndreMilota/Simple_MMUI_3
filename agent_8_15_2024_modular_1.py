# This module connects the agent core with the application and starts everything running.

from tool_box import Tool_Box
from typing import Tuple
import agent_core as AC
import GUI_4 as GUI
import GUI_stub_wrapper as GUI_Offline
import offline_tests_2 as OT
from agent_core import Agent_Core
from gesture_manager import Gesture_Manager

def load_tools(gui) -> Tool_Box:
    out = Tool_Box()

    # add the tools here
    #def set_button_color(button_index: int, color_name: str) -> str
    # returns a string and a bool to indicate that more actions are needed
    def set_button_color(button_index: int, color_name: str) -> Tuple[str, bool]:
        """Set the background color of a button."""
        gui.set_button_color(button_index, color_name)
        out = f"Set button {button_index} to {color_name}"
        return out, False

    # todo we could use something to make this easier
    example = [
        # give an example of a command
        {
            "role": "user",
            "content": "Make this white. Button 1 was indicated"  # todo update this to use the gesture manager
        },
        {
            "role": "assistant",
            'tool_calls': [
                {
                    'id': 'call_ywm8',
                    'function': {
                        'name': 'set_button_color',
                        'arguments': '{"button_index": 1, "color_name": "white"}'
                        # earlyer we used red but I am afraid it will interfear with
                    },
                    'type': 'function'
                }
            ]
        }
    ]

    # todo we need a way to keep the variable names in sync with the names used in the examples or at least check to see
    # if they are in consistent

    description = "Sets a button to a given color"
    parameters = {
        "button_index": {
            "type": "integer",
            "description": "The index of the button to change the color of. "
                           "Buttons are numbered starting from 0 up to n - 1.",
        },
        "color_name": {
            "type": "string",
            "description": "The name of the color to change the button to",
        },
    }

    out.add_tool_mandatory_args(tool=set_button_color, description=description, parameters=parameters, example=example)

    # ------------------------------------------------------------------------------
    # add an example of copying a property from one object to  another using gestures and a command
    gm = Gesture_Manager()
    gm.button_clicked(1)
    gm.button_clicked(2)
    key_content = "Copy the color from here to here. " + gm.get_description()
    example_2 = [
        # give an example of a command
        {
            "role": "user",
            "content": "Make button two green."
        },
        {
            "role": "assistant",
            'tool_calls': [
                {
                    'id': 'call_ywm5',
                    'function': {
                        'name': 'set_button_color',
                        'arguments': '{"button_index": 1, "color_name": "green"}'
                    },
                    'type': 'function'
                }
            ]
        },
        {
            "role": "user",
            "content": key_content
        },
        # # now we need to add the example of doing it now that we have set up the state
        # # {
        # #     "role": "user",
        # #     "content": "Make button two the same color as button one."
        # # },
        # now it needs to get the color
        {
            "role": "assistant",
            'tool_calls': [
                {
                    'id': 'call_ywm4',
                    'function': {
                        'name': 'get_button_color',
                        'arguments': '{"button_index": 1}'
                    },
                    'type': 'function'
                }
            ]
        },
        {
            "tool_call_id": 'call_ywm4',
            "role": "tool",
            "name": 'get_button_color',
            "content": "green",
        },
        # now it needs to set the color
        {
            "role": "assistant",
            'tool_calls': [
                {
                    'id': 'call_ywm1',
                    'function': {
                        'name': 'set_button_color',
                        'arguments': '{"button_index": 2, "color_name": "green"}'
                    },
                    'type': 'function'
                }
            ]
        },
    ]

    out.add_example(example_2)
    # ------------------------------------------------------------------------------
    # add the get_button_color tool
    def get_button_color(button_index: int) -> Tuple[str, bool]:
        """Get the background color of a button."""
        out = gui.get_button_color(button_index)
        return out, True

    example = None

    description = "Gets the color of a button"
    parameters = {
        "button_index": {
            "type": "integer",
            "description": "The index of the button to get the color of. "
                           "Buttons are numbered starting from 0 up to n - 1.",
        },
    }

    out.add_tool_mandatory_args(tool=get_button_color, description=description, parameters=parameters, example=example)

    # more tools go here
    # def print_thoughts(thoughts :str) -> Tuple[str, bool]:
    #     print("Thouts = ", thoughts)
    #     return "printed text", False
    # example = None
    #
    # description = "Prints text to the console. The LLM can use this for train of thought reasoning and debugging."
    # parameters = {
    #     "thoughts": {
    #         "type": "string",
    #         "description": "The text to print to the console.",
    #     },
    # }
    #
    # out.add_tool_mandatory_args(tool=print_thoughts, description=description, parameters=parameters, example=example)

    return out


class Agent(Agent_Core):
    def __init__(self, gui):
        self.gui = gui
        self.tool_box = load_tools(gui)
        # init the base class
        super().__init__(self.tool_box, gui)

    def get_gui(self):
        return self.gui

    def get_tool_box(self):
        return self.tool_box

    def get_prompt_assembler(self):
        return self.prompt_assembler

    def reset(self):
        self.gui.reset()

def run_MMUI():
    gui = GUI.Window()
    agent = Agent(gui)
    gui.run()


import offline_query_tests_3 as OLQT


def main():
    # for offline testing
    gui = GUI_Offline.Window("agent_8_15_2024_modular_1")
    mmui = Agent(gui)
    mmui.reset()
    #OLQT.deictic_query_test(mmui)
    #OT.simple_deictic_test(mmui)
    # OT.simple_description_test(mmui)
    # OT.simple_question_test(mmui)
    OLQT.run_offline_tests(mmui)


if __name__ == "__main__":
    main()
