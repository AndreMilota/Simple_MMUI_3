# This class combines the Prompt assembler and the response processor and connects to the llm
# it will contain the main Loop that calls the llm multiple times
# An external file will have to connect it to the application by loading tools into the toolbox and potentially
# setting other variables such as the core prompt


from prompt_assembler import Prompt_Assembler
from tool_box import Tool_Box
import os
import json
from groq import Groq
from typing import Callable, Any


# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )

# todo move pretty_print to a test file
def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))
class Agent_Core():
    def __init__(self, tool_box: Tool_Box, gui, core_prompt = None):
        self.tool_box = tool_box
        self.prompt_assembler = Prompt_Assembler(tool_box, core_prompt)
        self.available_functions = tool_box.available_functions   # we just link to it without a function as this will remain the same for all commands
        self.gui = gui
        def callback_function(command, gestures):
            messages = self.prompt_assembler.compute_prompt(command, gestures)
            tools = self.tool_box.get_tools(command)

            # print("messages", messages)
            # pretty_print(messages)
            # print("tools", tools)
            # pretty_print(tools)
            # call the LLM
            response = client.chat.completions.create(  # <------ call the LLM
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=4096
            )

            # process the response all we can deal with now is a list of function calls
            # process the response all we can deal with now is a list of function calls
            response_message = response.choices[0].message
            print("response_message = ", response_message)
            tool_calls = response_message.tool_calls
            if tool_calls:
                # messages.append(response_message)
                print("tool_calls length = ", len(tool_calls))
                print("tool_calls = ", tool_calls)
                for tool_call in tool_calls:
                    print("tool_calls length in loop = ", len(tool_calls))
                    print("tool_calls in loop = ", tool_calls)
                    print("tool_call = ", tool_call)
                    function_name = tool_call.function.name
                    function_to_call = self.available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)

                    # for testiing get a list of the arguments the function takes
                    args = function_to_call.__code__.co_varnames
                    print("args = ", args)

                    function_response = function_to_call(**function_args)

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
            # self.gui.set_run_callback(self.callback_function) this was set in the constructor
            self.gui.run()

