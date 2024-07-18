#agent_1.py
# uses open AI
import GUI_4 as GUI

# inports
# had to install "python-dotenv" to get this to work. I could not get dotenv to work it gave me an error
from dotenv import load_dotenv
_ = load_dotenv()

# installed langgraph, openai,
# installed langchain_openai from the terminal could not find it in the file settings list
# pip install langchain_openai
# alse installed pip install pygraphviz
# pip install langgraph
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory


#  python.exe -m pip install --upgrade pip
# pip install --upgrade langchain-community
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.agents import tool
# pip install ipython
from IPython.display import Image

# tool = TavilySearchResults(max_results=4) #increased number of results
# print(type(tool))
# print(tool.name)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system # system message
        self.memory = ConversationBufferMemory(return_messages=True)

        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0
    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages

        # Add memory to the messages
        memory_messages = self.memory.load_memory_variables({})["history"]
        messages = memory_messages + messages

        message = self.model.invoke(messages)

        # Save the interaction to memory
        self.memory.save_context({"input": messages[-1].content}, {"output": message.content})

        return {'messages': [message]}
    # def call_openai(self, state: AgentState):
    #     messages = state['messages']
    #     if self.system:
    #         messages = [SystemMessage(content=self.system)] + messages
    #     message = self.model.invoke(messages)
    #     return {'messages': [message]}
    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}



prompt_template = """You are a multimodal agent for controlling a simple app. \
You will be given the text of the commands the user issues. \
If the user also makes a gesture along with the command you will be given a description. \
of any gestures the user made during the turn. \
The app lets users set the color of buttons. \
There are {number_of_bs} buttons. \
Button indexis start at 0. \
Buttions 0 is above 1 and 2 is below 1 etc. \
Also you can answer random questions that don't result in the changing of the button's state.

Previous conversation:
{history}

[Verbal command]: {command}
[Gesture description]: {gestures}"""


def run_MMUI(prompt_template=prompt_template, model=None, ASR_wrapper=None, gui=None, window_name="agent_2 with ASR gui 4"):
    if model is None:
        model = ChatOpenAI(model="gpt-3.5-turbo")
    if gui is None:
        gui = GUI.Window(window_name,number_of_buttons=3)

    # modify the prompt to reflect the number of buttons
    nunber_of_buttons = gui.get_number_of_buttons()

    @tool
    def set_button_color(button_index: int, new_color: str) -> None:
        """Set the background color of a button."""
        gui.set_button_color(button_index, new_color)

    abot = Agent(model, [set_button_color], system=prompt_template)
    # this does not work for some
    # tools = gui.get_tools()
    # abot = Agent(model, tools, system=prompt_template)


    def callback_function(command, gestures):
        prompt = prompt_template.format(
            number_of_bs=nunber_of_buttons,
            history=abot.memory.load_memory_variables({})["history"],
            command=command,
            gestures=gestures
        )
        messages = [HumanMessage(content=prompt)]
        result = abot.graph.invoke({"messages": messages})
        print(result)

    gui.set_run_callback(callback_function)
    gui.run()

def main():
    run_MMUI()

if __name__ == "__main__":
    main()