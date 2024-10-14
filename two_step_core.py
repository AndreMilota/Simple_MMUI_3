# This module encapsulates a two-step agent core. It takes two toolboxes and two sets of instructions.
# The first set of instructions is run with the first toolbox. If calls are made in this stage,
# the second set of instructions and toolbox are used to invoke the LLM a second time.
# In addition to calling the LLM with different sets of instructions, it encapsulates how the results
# from the initial calls are incorporated into the prompt for the second call.

import pprint
from prompt_assembler import Prompt_Assembler
from tool_box import Tool_Box
import os
import json
from groq import Groq
from model_manager import get_model_call, identify_model
from typing import Callable, Any, Tuple
from test_utills import pretty_print

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )

class Two_Stage_LLM_Processor:
    def __init__(self, prompt_assemblers: list[Prompt_Assembler]) -> Tuple[bool, str]:
        self.prompt_assemblers = prompt_assemblers
        self.models = [MODEL, MODEL]
        self.model_calls = [get_model_call(model) for model in self.models]
        self.services = [identify_model(model) for model in self.models]

    def step(self, command, gestures="", response=None, index=0):
        assembler = self.prompt_assemblers[index]
        message = assembler.compute_prompt(command, gestures, response)
        tool_box = self.prompt_assemblers[index].tool_box
        tools = tool_box.get(platform=self.services[index], command=command)

        response = self.model_calls[index](  # <------ call the LLM
            model=self.models[index],
            messages=message,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096,
            temperature=0.0
        )

        return response

    def process_response(self, response, index = 0) -> Tuple[str, bool]: # if true you need to use the other in a call to the LLM for a second round
        text_out = ""
        tool_box = self.prompt_assemblers[index].tool_box
        available_functions = tool_box.available_functions
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        text_out = ""
        need_another_turn = False
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                function_response = function_to_call(**function_args)
                #print("function_response = ", function_response)

                output, flag = function_response
                if flag:
                    need_another_turn = True
                    text_out += output
            return text_out, need_another_turn
        else:
            return response_message.content, False

    def process_command(self, command, gestures):
        r0 = self.step(command, gestures, index=0)
        text, flag = self.process_response(r0, index=0)
        if flag:
            r1 = self.step(command, gestures, response=text, index=1)
            text, flag = self.process_response(r1, index=1)
        return text


