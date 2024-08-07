# this is an agent implemented with llama and Groq but not langchain
import os
import json
from groq import Groq
import GUI_4 as GUI

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')

MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )


def run_MMUI(ASR_wrapper=None, gui=None, window_name=None):
    if not gui:
        if not window_name:
            # get the python file name
            window_name = os.path.basename(__file__).split(".")[0]
        gui = GUI.Window(number_of_buttons=3, transcriber=ASR_wrapper, title=window_name)

        nunber_of_buttons = gui.get_number_of_buttons()

        # define the tools
        def set_button_color(button_index: int, new_color: str) -> str:
            """Set the background color of a button."""
            gui.set_button_color(button_index, new_color)
            out = f"Set button {button_index} to {new_color}"
            return out

        # assemble the prompt template
        prompt_core = """You are a multimodal agent for controlling a simple app.
        You will be given the text of the commands the user issues and if they make any gestures you will a description of them.
        The application you are controlling  has {nunber_of_buttons} buttons.
        You can set there by calling the function called set_button_color.
        It takes two arguments, the index of the button and the color you want to set it to.
        it will return something like 'Set button 1 to red'."""

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

    # register the callback function for the GUI
    def callback_function(command, gestures):
        c_and_g = f"{command} "

        if gestures:
            c_and_g += gestures

        messages = [
            {
                "role": "user",
                "content": prompt_core
            },
            {
                "role": "user",
                "content": c_and_g,
            }
        ]

        # call the LLM
        response = client.chat.completions.create(
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
            messages.append(response_message)
            print("tool_calls length = ", len(tool_calls))
            print("tool_calls = ", tool_calls)
            for tool_call in tool_calls:
                print("tool_calls length in loop = ", len(tool_calls))
                print("tool_calls in loop = ", tool_calls)
                print("tool_call = ", tool_call)
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(
                    expression=function_args.get("expression")
                )
                print("function_response = ", function_response)


    gui.set_run_callback(callback_function)
    gui.run()


def main():
    run_MMUI()


if __name__ == "__main__":
    main()

# def calculate(expression):
#     """Evaluate a mathematical expression"""
#     print(f"Evaluating expression: {expression}")
#     try:
#         result = eval(expression)
#         return json.dumps({"result": result})
#     except:
#         return json.dumps({"error": "Invalid expression"})
#
# def run_conversation(user_prompt):
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a calculator assistant." +
#                        "Use the calculate function to perform mathematical operations and provide the results." +
#                        "keep the answer as short as possible"
#
#         },
#         # give it an example
#         {
#             "role": "user",
#             "content": "what is 5 * 2 - 8?"
#         },
#         {
#             'role': 'assistant',
#             'tool_calls': [
#                 {
#                     'id': 'call_ywm8',
#                     'function': {
#                         'arguments': '{"expression": "5 * 3 - 8"}',
#                         'name': 'calculate'
#                     },
#                     'type': 'function'
#                 }
#             ]
#         },
#         {
#             'tool_call_id': 'call_ywm8',
#             'role': 'tool',
#             'name': 'calculate',
#             'content': '{"result": 7}'
#         },
#         # put in the systmes responce here
#         {
#             "role": "assistant",
#             "content": "7"
#         },
#         {
#             "role": "user",
#             "content": user_prompt,
#         }
#     ]
#     tools = [
#         {
#             "type": "function",
#             "function": {
#                 "name": "calculate",
#                 "description": "Evaluate a mathematical expression with more then one operator like 25 * 4 + 10",
#                 "parameters": {
#                     "type": "object",
#                     "properties": {
#                         "expression": {
#                             "type": "string",
#                             "description": "The mathematical expression to evaluate",
#                         }
#                     },
#                     "required": ["expression"],
#                 },
#             },
#         }
#     ]
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=messages,
#         tools=tools,
#         tool_choice="auto",
#         max_tokens=4096
#     )
#
#     response_message = response.choices[0].message
#     print("response_message = ", response_message)
#     tool_calls = response_message.tool_calls
#     if tool_calls:
#         available_functions = {
#             "calculate": calculate,
#         }
#         messages.append(response_message)
#         print("tool_calls length = ", len(tool_calls))
#         print("tool_calls = ", tool_calls)
#         for tool_call in tool_calls:
#             print("tool_calls length in loop = ", len(tool_calls))
#             print("tool_calls in loop = ", tool_calls)
#             print("tool_call = ", tool_call)
#             function_name = tool_call.function.name
#             function_to_call = available_functions[function_name]
#             function_args = json.loads(tool_call.function.arguments)
#             function_response = function_to_call(
#                 expression=function_args.get("expression")
#             )
#             print("function_response = ", function_response)
#             messages.append(
#                 {
#                     "tool_call_id": tool_call.id,
#                     "role": "tool",
#                     "name": function_name,
#                     "content": function_response,
#                 }
#             )
#         second_response = client.chat.completions.create(
#             model=MODEL,
#             messages=messages
#         )
#         return second_response.choices[0].message.content
#
# #user_prompt = "What is 25 * 4 + 10?"
# user_prompt = "What is 321 * 163 + 123 * 162?"
# r = run_conversation(user_prompt)
# print("r = ", r)
