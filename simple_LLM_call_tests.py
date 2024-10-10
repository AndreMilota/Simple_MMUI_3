import pprint
from prompt_assembler import Prompt_Assembler
from tool_box import Tool_Box
import os
import json
from groq import Groq
from typing import Callable, Any
from test_utills import pretty_print
from tool_box import Tool_Box

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = "gpt-4"
#MODEL = 'llama3-groq-70b-8192-tool-use-preview'
#MODEL = 'llama-3.1-70b-versatile'
# get the key and create a client
client = Groq(api_key=groq_key, )

from agent_8_15_2024_modular_1 import load_tools

class Molk_GUI():
    def get_button_color(self, button_index):
        print("get_button_color", button_index)
        return "red"

    def get_number_of_buttons(self):
        print("get_number_of_buttons")
        return 3

    def set_button_color(self, button_index, color_name):
        print("set_button_color", button_index, color_name)
        pass

# instructions_1 = """You are a multimodal agent who controls a simple application for the user.
#  the user May issue either commands or questions and these may or may not be accompanied
#  by one or more gestures.
# If gestures are present they will be described in the prompt.
# Please rewrite the users input To integrate the gestures with the utterances."""


instructions_1 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without a gestures.
Than make a list of the information you would need to accomplish the action."""

instructions_2 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action.
You are given functions that take the index of the button and return its color and another 
function that given the index of a button and a color will set the buttons color.
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change. 
"""
instructions_3 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action and explain why you need this information.
You are given functions that take the index of the button and return its color and another 
function that given the index of a button and a color will set the buttons color.
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change."""

instructions_4 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action.
You are given functions that take the name of the button and return its color and another 
function that given the name of a button and a color will set the buttons color.
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change. """
# did not make any function calls


instructions_5 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action.
You are given functions that take the name of the button and return its color and another 
function that given the name of a button and a color will set the buttons color.
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change. """
# ignors the last line of the prompt
# once I gave it tools it use the rong index for the button

instructions_6 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action.
You are given functions that take the name of the button and return its color and another 
function that given the name of a button and a color will set the buttons color.
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change. 
If you do not make any function calls explain why.
"""
# this seems to work for the "The user said: make this the color of this"
# but when I swap the gesters it files with the tools
# this gets confused if the user points to 1 and 2 it gets the color of 1 rather then 2 it looks like it is making an off by one error assuming that indexes start at 1

instructions_7 = """Please take the multimodal input which consists of an utterance and a 
description of a gesture and rewrite it Expressing the same ideas but without the gestures.
Than make a list of the information you would need to accomplish the action.
You are given functions that take the name of the button and return its color and another 
function that given the name of a button and a color will set the buttons color.
Button indexes start at 0, and if the user points to or says 'button 1' then they mean the button at index 1. 
Next if you can call a function to get this information invoke that tool.
Alternately if you have all the information you need to make the requested action happen then call the function
that will make the change. 
If you do not make any function calls explain why.
"""
instructions_8 = """You are controlling a simple application through tool calls. 
User input will consist of text they speak and sometimes descriptions of gestures they make.
Integrate their utterances and resolve pronouns using the descriptions of the gestures.
Then consider what information you need to answer their question or take the action they request.
When information is required, such as the color of a button, make the appropriate function call.
If you have the appropriate information available and they have requested an action, 
make the appropriate function call to take that action.
You are given a function which gets the color of a button given its number and a second function 
that sets the button’s color, given its number and the desired color you want to set it to. 
"""
# this makes all the calls in one go and files

# prompt = [{
#             "role": "assistant",
#             "content": instructions_7
#         }]
#
# #message = "The user said: make this blue. While making a gesture that indicated Button 1"
# message = ("""The user said: 'make this the color of this.',
#            While making a gesture that indicated 'Button 2' and then another indicating 'Button 1'""")
# # it is importnat to put the '' around the button names
# # if you capatalize make it will get it wrong
#
# prompt += [{"role": "user", "content": message}]
#
# # tools
# molk_gui = Molk_GUI()
# tool_box = load_tools(molk_gui)
# #tool_box = Tool_Box()
#
# tools = tool_box.get_tools("nothing")
#
# response = client.chat.completions.create(  # <------ call the LLM
#                     model=MODEL,
#                     messages=prompt,
#                     tools=tools,
#                     tool_choice="auto",
#                     max_tokens=4096,
#                     temperature = 0.0
#                 )
# print("-----------------------------------------------------------------------------------------------------")
# print(response.choices[0].message)