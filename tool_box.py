#This class maintains a list of tools that are embedded in tool wrappers.
# It may also include examples of multi-tool use.
# The class can be extended or wrapped to provide RAG-like capabilities for selecting tools whose information needs to
# be included in a prompt. Additionally, this class will be used by the parser to retrieve a list of tools
import inspect
from tool_wrapper import Tool_Wrapper

class Tool_Box:
    def __init__(self):
        self.available_functions = {}
        self.tool_descriptions = []
        self.tool_examples = []

    def add_tool(self, tool: Tool_Wrapper):
       # get the name of the tool using the inspect module
        name = tool.function.__name__
        self.available_functions[name] = tool
        self.tool_descriptions.append(tool.instructions)
        self.tool_examples.append(tool.examples)


    def get_prompt_elements(self, command: str) -> tuple:

    def add_example(self, example: dict):


    def process_call_request(self, call_request: dict) -> str: