# This class combines the Prompt assembler and the response processor and connects to the llm
# it will contain the main Loop that calls the llm multiple times
# An external file will have to connect it to the application by loading tools into the toolbox and potentially
# setting other variables such as the core prompt
# this class does not know about the GUI, but it does know about the tool box
# and it provides a function for the GUI to call to get the next response

from prompt_assembler import Prompt_Assembler
from tool_box import Tool_Box

class Agent_Core():
    def __init__(self, tool_box, core_prompt):
        self.tool_box = tool_box

        self.prompt_assembler = Prompt_Assembler(tool_box, core_prompt)

