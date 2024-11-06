# SQL_core.py is a module that implements a two-step core that uses SQL in the first step

import pprint

from annotated_types.test_cases import cases

from SQL_prompt_assembler import Primary_Prompt_Assembler
#from tool_box import Tool_Box
import os
import json
from groq import Groq
from model_manager import get_model_call, identify_model
from typing import Callable, Any, Tuple
import database
# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
#MODEL = 'gpt-4o'
# get the key and create a client
client = Groq(api_key=groq_key, )

def contains_SQL(text):
    return "<SQL>" in text and "</SQL>" in text

class SQL_Core:
    def __init__(self, colors=["red", "green", "blue"]):
        self.database = database.Database(colors)
        print(self.database.get_number_of_buttons())

        pa1 = Primary_Prompt_Assembler(self.database)
        pa2 = Primary_Prompt_Assembler(self.database)
        self.prompt_assemblers = [pa1, pa2]
        self.models = [MODEL, MODEL]
        self.model_calls = [get_model_call(model) for model in self.models]

    def step(self, command, gestures="", response=None, index=0):
        assembler = self.prompt_assemblers[index]
        message = assembler.compute_prompt(command, gestures, response)

        response = self.model_calls[index](  # <------ call the LLM
            model=self.models[index],
            messages=message,
            tools=None,
            tool_choice="auto",
            max_tokens=4096,
            temperature=0.0
        )
        return response

    def process_SQL(self, text):
        sql = text[text.find("<SQL>") + 5:text.find("</SQL>")]
        print(sql)

        # apply the SQL to the database
        self.database.cursor.execute(sql)
        self.database.conn.commit()
        return sql, True

    def process_response(self, response, index = 0) -> Tuple[str, bool]: # if true you need to use the other in a call to the LLM for a second round
        #tool_box = self.prompt_assemblers[index].tool_box
        available_functions = set()
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        text_out = ""
        need_another_turn = False
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                if function_name not in available_functions:
                    print(f"Function {function_name} not found in available functions")
                    return response_message.content, False
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                function_response = function_to_call(**function_args)
                # print("function_response = ", function_response)

                output, flag = function_response
                if flag:
                    need_another_turn = True
                    text_out += output
            return text_out, need_another_turn

        if contains_SQL(response_message.content):
            return self.process_SQL(response_message.content)

        return response_message.content, False

    def process_command(self, command, gestures):
        r0 = self.step(command, gestures, index=0)
        text, flag = self.process_response(r0, index=0)
        # if flag:
        #     r1 = self.step(command, gestures, response=text, index=1)
        #     text, flag = self.process_response(r1, index=1)
        return text

def main():

    core = SQL_Core(["green", "green", "green", "blue", "green", "green", "green"])
    #command = "What color are carrots typically?"
    gestures = ""

    command = "Make all the green buttons red."

    print(core.process_command(command, gestures))

    database = core.database
    c = database.get_button_colors()
    print(c)

if __name__ == "__main__":
    main()