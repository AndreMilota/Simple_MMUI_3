#This class maintains a list of tools that are embedded in tool wrappers.
# It may also include examples of multi-tool use.
# The class can be extended or wrapped to provide RAG-like capabilities for selecting tools whose information needs to
# be included in a prompt. Additionally, this class will be used by the parser to retrieve a list
# of tools

import inspect
from typing import Callable, Any
import json
from typing import List, Any

def flatten_list(list_of_lists: List[List[Any]]) -> List[Any]:
    return [item for sublist in list_of_lists for item in sublist]
def pretty_print(obj: Any) -> None:
    print(json.dumps(obj, indent=4))

class Tool:
    def __init__(self, tool, name: str, description: str):
        self.function = tool
        self.name = name
        self.description = description
        self.parameters = {}
        self.examples = []
        self.required_parameters = []

    def add_parameter(self, name: str, description: str, type: str = "string", legal_values: List[str] = None):
        # assert that it is not a duplicaed definition
        assert name not in self.parameters.keys()
        if legal_values is None:
            self.parameters[name] = {
                "type": type,
                "description": description,
            }
        else:
            self.parameters[name] = {
                "type": type,
                "description": description,
                "legal_values": legal_values
            }

    def add_required_parameter(self, name: str, description: str, type: str, legal_values: List[str] = None):
        self.required_parameters.append(name)
        self.add_parameter(name, description, type, legal_values)

    def add_example(self, example: dict):
        self.examples.append(example)

    def get(self):
        parameters = {
            "type": "object",
            "properties": self.parameters,
        }
        if self.required_parameters != []:
            parameters["required"] = self.required_parameters
        out = {
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters,
            }
        }

        out["type"] = "function"
        return out

    def call(self, **kwargs):
        return self.function(**kwargs)

class Tool_Box:
    def __init__(self):
        self.available_functions = {}  # this is used to process the call requests
        #self.tool_examples = []  # this is used to generate the prompt to give the LLM of examples of tool use it may not have a one to one mapping with the tools

    def add_tool(self, tool: Tool):
        # add to available_functions
        self.available_functions[tool.name] = tool

    def process_call_request(self, call_request: dict) -> str:
        # get the tool
        tool = self.available_functions[call_request['id']]
        # get the arguments
        arguments = call_request['function']['arguments']
        # call the function
        return tool(**arguments)

    def get_tools(self, name: str) -> list:
        out = []
        for t in self.available_functions.values():
            out += [t.get()]
        return out
