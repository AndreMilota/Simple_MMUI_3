# This set of classes is used to manage tool representations.

from typing import List, Any, Union
import json

# This class is used to manage a single parameter.
class Parameter:
    def __init__(self, name: str, description: str, type: str = "string", legal_values: List[str] = None):
        self.name = name
        self.description = description
        self.type = type
        self.legal_values = legal_values

    def get(self, platform :str  = "groq"):
        if platform == "groq":
            out = {
                "type": self.type,
                "description": self.description,
            }
            if self.legal_values:
                out["legal_values"] = self.legal_values

        elif platform == "open_ai":
            out = {
                "name": self.name,
                "description": self.description,
            }
            if self.legal_values:
                out["legal_values"] = self.legal_values
        else:
            raise ValueError(f"Unknown platform: {platform}")
        return out

# This class is used to manage a single tool.
class Tool:
    def __init__(self, tool, name: str, description: str):
        self.function = tool
        self.name = name
        self.description = description
        self.parameters = {}
        self.required_parameters = []

    def add_parameter(self,
                      parameter_or_name: Union[Parameter, str],
                      description: str = None,
                      type: str = "string",
                      legal_values: List[str] = None):
        if isinstance(parameter_or_name, str):
            name = parameter_or_name
            parameter = Parameter(name, description, type, legal_values)
        else:
            parameter = parameter_or_name
        assert parameter.name not in self.parameters.keys()

        self.parameters[parameter.name] = parameter


    def add_required_parameter(self,
                               parameter_or_name: Union[Parameter, str],
                               description: str,
                               type: str,
                               legal_values: List[str] = None):
        self.add_parameter(parameter_or_name, description, type, legal_values)

        if isinstance(parameter_or_name, str):
            name = parameter_or_name
        else:
            name = parameter_or_name.name

        self.required_parameters.append(name)


    def get(self, platform :str  = "groq" ):
        parameters = {
            "type": "object",
            "properties": {name: parameter.get(platform) for name, parameter in self.parameters.items()},
        }
        if self.required_parameters:
            parameters["required"] = self.required_parameters

        out = {
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters,
            }
        }

        if platform == "groq":
            out["type"] = "function" #changing this at recomendation of chatgpt
        elif platform == "open_ai":
            out["type"] = "function"
        else:
            raise ValueError("platform must be 'groq' or 'open_ai'")
        return out

    # call the function
    def __call__(self, **kwargs):
        return self.function(**kwargs)

# This class is used to manage a collection of tools.
class Tool_Box:
    def __init__(self):
        self.available_functions = {}  # this is used to process the call requests
        #self.tool_examples = []  # this is used to generate the prompt to give the LLM of examples of tool use it may not have a one to one mapping with the tools

    def add_tool(self, tool: Tool):
        # add to available_functions
        self.available_functions[tool.name] = tool

    # def process_call_request(self, call_request: dict) -> str:
    #     # get the tool
    #     tool = self.available_functions[call_request['id']]
    #     # get the arguments
    #     arguments = call_request['function']['arguments']
    #     # call the function
    #     return tool(**arguments)

    def process_call_request(self, call_request: dict) -> str:
        tool = self.available_functions[call_request['id']]
        arguments = call_request['function']['arguments']

        # Check if all required parameters are present
        missing_params = [param for param in tool.required_parameters if param not in arguments]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")

        # Safely call the function with arguments
        try:
            return tool.function(**arguments)
        except TypeError as e:
            raise ValueError(f"Error in function call: {str(e)}")

    def get(self, platform :str  = "groq", command :str = None) -> list:
        """ Returns the data structure which is supposed to be used as the tools list and will be given to the llm."""
        out = []
        for tool in self.available_functions.values():
            out.append(tool.get(platform))
        return out
