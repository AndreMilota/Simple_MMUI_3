# this is an agent implemented with llama and Groq but not langchain
import os
import json
from groq import Groq
import GUI_4 as GUI
import GUI_stub_wrapper as GUI_Offline # for testing
import offline_tests_2 as OT

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )

MMUI_GUI = False # TODO figure out how to make this a class member variable in a way that the call backe can us eit

prompt_core = """You are a multimodal agent for controlling a simple app.
You will be given the text of the commands the user issues and if they make any gestures you will be given a description of them.
The application you are controlling has {number_of_buttons} buttons.
You can set there by calling the function called set_button_color.
It takes two arguments, the index of the button and the color you want to set it to.
it will return something like 'Set button 1 to red'.
The user may also ask a question that does not entail making a function call.
When asked a question answer with a brief response unless the user asks for you to provide longer responses."""

class MMUI:
    def __init__(self, gui=None, window_name=None):
        if not gui:
            if not window_name:
                # get the python file name
                window_name = os.path.basename(__file__).split(".")[0]
            gui = GUI.Window(number_of_buttons=3, title=window_name)
        MMUI_GUI = gui # TODO WE MAY REMOVE THIS LINE
        self.gui = gui
        number_of_buttons = gui.get_number_of_buttons()

        def set_button_color(button_index: int, new_color: str) -> str:
            """Set the background color of a button."""
            MMUI_GUI.set_button_color(button_index, new_color)
            out = f"Set button {button_index} to {new_color}"
            return out

        tools = [
            {
                "type": "function",
                "function": {
                    "name": "set_button_color",
                    "description": "Sets a button to a given color",
                    "parameters": {
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
                    },
                },
            }
        ]

        prompt = [
            {
                "role": "assistant",
                "content": prompt_core
            }]

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
        # register the callback function for the GUI
        def callback_function(command, gestures):
            c_and_g = f"{command} "

            if gestures:
                c_and_g += gestures

            messages = prompt + example + [
                {
                    "role": "user",
                    "content": c_and_g
                }
            ]

            # call the LLM
            response = client.chat.completions.create(  # <------ call the LLM
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=4096
            )

            # process the response all we can deal with now is a list of function calls
            response_message = response.choices[0].message
            print("response_message = ", response_message)
            tool_calls = response_message.tool_calls
            if tool_calls:
                available_functions = {
                    "set_button_color": set_button_color,
                }
                #messages.append(response_message)
                print("tool_calls length = ", len(tool_calls))
                print("tool_calls = ", tool_calls)
                for tool_call in tool_calls:
                    print("tool_calls length in loop = ", len(tool_calls))
                    print("tool_calls in loop = ", tool_calls)
                    print("tool_call = ", tool_call)
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    button_index = function_args.get("button_index")
                    new_color = function_args.get("color_name")

                    function_response = function_to_call(button_index, new_color)

                    print("function_response = ", function_response)
                return ""
            else:
                return response_message.content

        gui.set_run_callback(callback_function)

    def reset(self):
        self.gui.reset()

    def get_gui(self):
        return self.gui

    def run(self):
        #self.gui.set_run_callback(self.callback_function) this was set in the constructor
        self.gui.run()

def main():
    # to run it normaly
    # gui = GUI.Window("window_name")
    # mmui = MMUI(gui)
    # mmui.run()

    # to run it with offline tests
    gui = GUI_Offline.Window("window_name")
    mmui = MMUI(gui=gui)
    OT.simple_dectic_test(mmui)


if __name__ == "__main__":
    main()
