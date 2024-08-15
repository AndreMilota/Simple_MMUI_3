#This class maintains a list of tools that are embedded in tool wrappers.
# It may also include examples of multi-tool use.
# The class can be extended or wrapped to provide RAG-like capabilities for selecting tools whose information needs to
# be included in a prompt. Additionally, this class will be used by the parser to retrieve a list of tools
import inspect
from typing import Callable, Any


class Tool_Box:
    def __init__(self):
        self.available_functions = {}
        self.tool_descriptions = []
        self.tool_examples = []

    def add_tool(self, tool: Callable[..., str], description :str, example: dict=None):
        # get the name of the tool using the inspect module
        name = tool.function.__name__
        self.available_functions[name] = tool
        if description:
            self.tool_descriptions.append(description)
        # TODO add something so we can pull the description out of the function using the inspect module
        if example:
            self.add_example(example)

    def get_prompt_elements(self, command: str) -> tuple:
        # we may want to add a function that returns the tool descriptions and examples
        return self.tool_descriptions, self.tool_examples

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