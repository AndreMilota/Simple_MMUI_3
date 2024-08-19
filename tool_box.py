#This class maintains a list of tools that are embedded in tool wrappers.
# It may also include examples of multi-tool use.
# The class can be extended or wrapped to provide RAG-like capabilities for selecting tools whose information needs to
# be included in a prompt. Additionally, this class will be used by the parser to retrieve a list of tools
import inspect
from typing import Callable, Any
import json
from typing import List, Any
def flatten_list(list_of_lists: List[List[Any]]) -> List[Any]:
    return [item for sublist in list_of_lists for item in sublist]
def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))

class Tool_Box:
    def __init__(self):
        self.available_functions = {}  # this is used to process the call requests
        self.tool_descriptions = []  # this is used to generate the prompt to let the LLM know what tools are available
        self.tool_examples = []  # this is used to generate the prompt to give the LLM of examples of tool use it may not have a one to one mapping with the tools

    def add_tool_mandatory_args(self, tool: Callable[..., str], description: str, parameters: dict,
                                example: list = None):
        # add to available_functions
        # get the name of the tool using the inspect module
        name = tool.__name__
        self.available_functions[name] = tool

        # add to tool_descriptions
        # get a list of all the properties
        parameters_list = list(parameters.keys())

        t_description = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": parameters,
                "required": parameters_list,
            },
        }

        self.tool_descriptions += [t_description]
        # pritty print the tool_descriptions
        print("Tool tool_descriptions:")
        pretty_print(self.tool_descriptions)

        for element in self.tool_descriptions:
            print(element, "\n")
        # TODO add something so we can pull the description out of the function using the inspect module

        if example:
            self.add_example(example)

    def add_example(self, example: dict):
        self.tool_examples.append(example)
        # todo add something so we can give examples with just a single string and have it create the dictionary element

    def process_call_request(self, call_request: dict) -> str:
        # get the tool
        tool = self.available_functions[call_request['id']]
        # get the arguments
        arguments = call_request['function']['arguments']
        # call the function
        return tool(**arguments)

    # TODO add RAG stuff to these functions to skale it
    def get_tools(self, command: str) -> list:
        return self.tool_descriptions

    def get_tool_examples(self, command: str) -> list:
        out = flatten_list(self.tool_examples)
        return out


