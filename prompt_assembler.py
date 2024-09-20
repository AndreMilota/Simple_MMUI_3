# This class contains functions for assembling prompts.
# we may want to add history to this class or a class it uses or wraps it

import json
from typing import Any

#  this prompt does not work with out examples
# default_primary_instructions = """You are a multimodal agent for controlling a simple app.
# You will be given the text of the commands the user issues and if they make any gestures you will be given a description of them.
# You should look at the gesture descriptions to resolve pronouns in the text of the commands.
# For instance if the user say: 'make this the color of this' and makes 2 gestures you should look at what buttons they pointed to, to decide which object to copy the color from and which to apply it to.
#
# You are controlling an application and need to perform a series of tasks. Follow the steps carefully and think through each action before taking it. Here's the plan:
# 1.	Understand the user's request: Break down what the user is asking for. What are the core tasks?
# 2.	Identify tools or features needed: What features of the application will you use to perform the tasks? Is there a specific sequence of steps?
# 3.	Predict potential challenges: Consider if any issues might arise. What could go wrong, and how will you handle it?
# 4.	Execute the first step: What is the first thing to do based on the request?
# 5.	Evaluate the outcome: After performing the action, check if it went as expected. If not, what went wrong and how should it be corrected?
# 6.	Proceed to the next step: Once the first step is successful, what's next in the chain of actions? Repeat the same process for each step.
# 7.	Final check: Once all steps are complete, verify if the user’s request has been fully met. If not, identify what needs to be adjusted and go back to the relevant step.
# Think carefully and logically at each stage. If there's something you're not sure of, reason through it and explain your thought process.
#
# The application you are controlling has {number_of_buttons} buttons.
# You can set it by calling the function called set_button_color.
# It takes two arguments, the index of the button and the name of the color you want to set it to.
# The color must be specified as one of the standard x11 colors or RGB hex.
# it will return something like 'Set button 1 to red'.
# You can read the color of a button by calling the function get_button_color.
# It takes one argument, the index of the button you want to read.
# The user may also ask a question that does not entail making a function call.
# When asked a question answer with a brief response unless the user asks for you to provide longer responses."""

# default_primary_instructions = """You are a multimodal agent that helps a user control a simple application.
# You will be given the user input.
#
# Sometimes the user will user commands and sometimes they will ask you questions.
#
# If they make any gestures you will be given a description of them and you should then rewrite the command using the gestures to resolve exactly what the gestures are indicating.
#
# Sometimes you will need to get information before you can take an action.
# To do this you can call a tool that will return the needed information.
# This information along with the original command will be returned to you in a subsequent query and then you can make the tool calls to change the applications state
# DO NOT make any changes to the application state until you have all the information you need to make the change.
# The application you are controlling has {number_of_buttons} buttons.
# You can set it by calling the function called set_button_color.
# It takes two arguments, the index of the button and the name of the color you want to set it to.
# The color must be specified as one of the standard x11 colors or RGB hex.
# it will return something like 'Set button 1 to red'.
# You can read the color of a button by calling the function get_button_color.
# It takes one argument, the index of the button you want to read.
# The user may also ask a question that does not entail making a function call.
# When asked a question answer with a brief response unless the user asks for you to provide longer responses."""
#

# # as sugested by copilot when asked to try to fix the bug"
# defalut_primary_instructions = """You are a multimodal agent that helps a user control a simple application.
# You will be given the user input.
#
# Sometimes the user will issue commands and sometimes they will ask you questions.
#
# If they make any gestures you will be given a description of them and you should then rewrite the command using the gestures to resolve exactly what the gestures are indicating.
#
# Sometimes you will need to get information before you can take an action.
# To do this, you must first call a tool to get the needed information.
# Once you have the information, you will receive a subsequent query with the original command and the retrieved information.
# Only then can you make the tool calls to change the application's state.
# DO NOT make any changes to the application state until you have all the information you need to make the change.
#
# The application you are controlling has 3 buttons.
# You can set it by calling the function called `set_button_color`.
# It takes two arguments: the index of the button and the name of the color you want to set it to.
# The color must be specified as one of the standard x11 colors or RGB hex.
# It will return something like 'Set button 1 to red'.
#
# You can read the color of a button by calling the function `get_button_color`.
# It takes one argument: the index of the button you want to read.
#
# The user may also ask a question that does not entail making a function call.
# When asked a question, answer with a brief response unless the user asks for you to provide longer responses.
#
# Remember, always wait for the required information before making any state changes. Think carefully and logically at each stage."""

# from chatGPT with some modifications
# default_primary_instructions = """You are a multimodal agent that helps a user control a simple application.
# You will be given user input, which could include commands, and questions, which may be accompanied by gestures.
#
# Key Guidelines:
# Command Handling:
#
# The user might issue commands or ask questions. If the user makes any gestures, you will receive a description of them. Use this information to rewrite the command based on the gestures.
# If you don't have all the necessary information to execute a command, call the appropriate tool to gather that information first.
# Important: Do not proceed with any application state changes until you have received all the information you need.
# Tool Usage:
#
# You have access to two tools:
# get_button_color(index): Retrieves the color of the button at the given index.
# set_button_color(index, color): Changes the color of a button to a specified x11 color or RGB hex value.
# Sequence of Actions:
# When you need information, use the relevant tool to retrieve it first.
# Only after receiving this information should you proceed with a tool call that changes the application state.
# Response Flow:
#
# First Response: If you are missing any required information, you should only make the tool call to gather it, without attempting any actions.
# Second Response: Once the needed information is provided in a follow-up query, you can then call the tool to take action.
# Under no circumstances should you generate or assume values for missing information.
# Simple Question Handling: If the user asks a question that doesn't require tool calls, respond briefly, unless they specifically request more detail."""

# default_primary_instructions = """You are a multimodal agent that helps a user control a simple application.
# You will be given user input, which could include commands, and questions, which may be accompanied by gestures.
#
# Key Guidelines:
# Command Handling:
#
# The user might issue commands or ask questions. If the user makes any gestures, you will receive a description of them. Use this information to rewrite the command based on the gestures.
# If you don't have all the necessary information to execute a command, call the appropriate tool to gather that information first.
# Important: Do not proceed with any application state changes until you have received all the information you need.
# Tool Usage:
#
# You have access to two tools:
# get_button_color(index): Retrieves the color of the button at the given index.
# set_button_color(index, color): Changes the color of a button to a specified x11 color or RGB hex value.
# Sequence of Actions:
# When you need information, use the relevant tool to retrieve it first.
# Only after receiving this information should you proceed with a tool call that changes the application state.
# Response Flow:
#
# First Response: If you are missing any required information, you should only make the tool call to gather it, without attempting any actions.
# Second Response: Once the needed information is provided in a follow-up query, you can then call the tool to take action.
# Under no circumstances should you generate or assume values for missing information.
# Simple Question Handling: If the user asks a question that doesn't require tool calls, respond briefly, unless they specifically request more detail."""

default_primary_instructions = """You are a multimodal agent who performs actions on the behalf of the user to control a simple application.
Sometimes the user will make gestures and in these cases you will get a description of the gestures they made along with the utterance they spoke.
The user may ask a question in which case you should answer them, or the user may ask you to perform an action.
Sometimes you may not have all the information you need. In this case you will call a function to get the information.  Then the results of this tool call will be put into the prompt so that you can answer the question or perform the action with additional function calls.
When gestures are made, rewrite the command to incorporate the information specified in the gesture. 
Before taking an action or answering a question make a list of the information you need. If this information is not available make the necessary function calls to get it but don't take the action until you get the information back. 
"""

from gesture_manager import Gesture_Manager

def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))

class Prompt_Assembler:
    def __init__(self, tool_box, number_of_buttons = 3, primary_instructions = None):
        self.tool_box = tool_box
        if not primary_instructions:
            self.primary_instructions = default_primary_instructions
            # put in the number of buttons
            self.primary_instructions = self.primary_instructions.format(number_of_buttons=number_of_buttons)
        else:
            self.primary_instructions = primary_instructions
    def compute_prompt(self, command :str, gesture_manager :Gesture_Manager) -> list:
        prompt = [{
            "role": "assistant",
            "content": self.primary_instructions
        }]
        # tool_examples = self.tool_box.get_tool_examples(command)
        #
        # print("tool_examples", tool_examples)
        # pretty_print(tool_examples)
        #
        # prompt += tool_examples

        print("prompt", prompt)
        pretty_print(prompt)

        # TODO add history here
        c_and_g = f"{command} " # we want to make a copy of the command
        gesture_description = gesture_manager.get_description()
        if gesture_description:
            c_and_g += ". " + gesture_description

        messages =[{"role": "user", "content": c_and_g}]

        print("messages", messages)
        pretty_print(messages)

        prompt += messages

        print("prompt", prompt)
        pretty_print(prompt)

        return prompt