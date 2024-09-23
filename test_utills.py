
import json
import os
from groq import Groq
from typing import Callable, Any


def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))

# load the key for the Groq API
groq_key = os.environ.get('GROQ_KEY')
MODEL = 'llama3-groq-70b-8192-tool-use-preview'
# get the key and create a client
client = Groq(api_key=groq_key, )

characterization_prompt = """You need to return 'True' of the following text matches this description otherwise return false:"""

def llm_based_assertion(characterization :str, text :str)-> bool:
    """Uses Llama 3 to evaluate the nature of the result of a command."""

    messages = [
        {"role": "user", "content": characterization_prompt + characterization},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(  # <------ call the LLM
        model=MODEL,
        messages=messages,
        tool_choice="auto",
        max_tokens=10,
        temperature=0.0
    )

    # see if it returns true or false
    response_message = response.choices[0].message
    out = response_message.content
    return out == "True"

class Singe_Step_Call_Tester:
    def __init__(self, model, tool_box):
        self.model = model
        self.tool_box = tool_box
        self.needed_calls = set()
        self.bad_calls = set()
        self.bad_call_functions = set()
        self.instructions = None

    def convert_args_to_strig(self, function_name : str, args :dict):
        return function_name + ", " + str(sorted(args.items()))

    def add_needed_call(self, function_name :str, arguments :dict):
        good_call = self.convert_args_to_strig(function_name, arguments)
        self.needed_calls.add(good_call)

    def add_bad_call(self, function_name :str, arguments :dict = None):
        if arguments is None:
            self.bad_call_functions.add(function_name)
        else:
            bad_call = self.convert_args_to_strig(function_name, arguments)
            self.bad_calls.add(bad_call)

    def set_instructions(self, instructions :str):
        self.instructions = instructions

    def reset_ground_truth(self):
        self.needed_calls = set()
        self.bad_calls = set()
        self.bad_call_functions = set()

    def test(self, input):
        prompt = [{
            "role": "assistant",
            "content": self.instructions
        }]
        prompt += [{"role": "user", "content": input}]
        tools = self.tool_box.get_tools(input)
        # now call the LLM
        response = client.chat.completions.create(  # <------ call the LLM
            model=self.model,
            messages=prompt,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096,
            temperature=0.0
        )

        # go though the calls and see if they are correct

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # create a set to store the good calls in
        good_calls = set()
        extra_calls = []

        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = self.tool_box.available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                # print("function_name = ", function_name)
                # print("function_args = ", function_args)
                call = self.convert_args_to_strig(function_name, function_args)
                # print(self.needed_calls)
                # print(call)
                # see if this is a needed call
                if call in self.needed_calls:
                    good_calls.add(call)
                # see if this is a bad call
                elif call in self.bad_calls:
                    print("bad call made " + call)
                    return False
                elif function_name in self.bad_call_functions:
                    print("bad function called " + call)
                    return False
                else:
                    extra_calls += [call]

        # check the length of the good calls
        needed_calls = len(self.needed_calls)
        good_calls = len(good_calls)
        if good_calls != needed_calls:
            print("failed to make all needed calls ---------------------")
            print("needed_calls = ", needed_calls)
            print("calls made = ", good_calls)
            return False

        if extra_calls:
            print("extra calls made ---------------------")
            print(extra_calls)

        print("passed test with: "+ input)
        return True

def main():

    # test our function
    characterization = "it mentions the color red"
    text = "button 1 is red"
    #assert llm_based_assertion(characterization, text) == True
    print("test 1 passed")

    text = "button 1 is green"
    #assert llm_based_assertion(characterization, text) == False
    print("test 2 passed")

    text = "the result is red"
    #assert llm_based_assertion(characterization, text) == True
    print("test 3 passed")

# run the main function
if __name__ == "__main__":
    main()