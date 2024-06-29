#agent_1.py
# TODO swap over to lama3
import GUI

# inports
# had to install "python-dotenv" to get this to work. I could not get dotenv to work it gave me an error
from dotenv import load_dotenv
_ = load_dotenv()

# installed langgraph, openai,
# installed langchain_openai from the terminal could not find it in the file settings list
# alse installed pip install pygraphviz
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os
from langchain.agents import tool
from IPython.display import Image

# tool = TavilySearchResults(max_results=4) #increased number of results
# print(type(tool))
# print(tool.name)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system # system message
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
        message = self.model.invoke(messages)
        return {'messages': [message]}

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
If the user also makes a gesture along with the command you will be given a description \
of any gestures the user made during the turn. The app lets users set the color of 2 buttons \
in the widget. \
Also you can answer random questions that done result in the changing of the button’s state.
[Verbal command]: {command}
[Gesture description]: {gestures}"""

def main():
    # create the window
    gui = GUI.Window("agent_1")
    # create the prompt

    # create a tool
    @tool
    def set_button_color(button_index: int, new_color: str) -> None:
        """Set the background color of a button. There are 2 buttons, 1 and 2"""
        print(f"Setting button {button_index} to {new_color}")
        #gui.todo = [button_index, new_color]
        gui.set_button_color(button_index, new_color)

    # create an agent
    model = ChatOpenAI(model="gpt-3.5-turbo")
    abot = Agent(model, [set_button_color], system=prompt_template)
    # link the agent up

    # this function gets called from the gui, it is given the command and the gestures
    def callback_function(command, gestures):
        # messages = [HumanMessage(content=command)]
        # input = {"messages": messages, "gestures": gestures}
        # result = abot.graph.invoke(messages)
        # Fill the prompt template with the command and gestures
        prompt = prompt_template.format(command=command, gestures=gestures)
        messages = [HumanMessage(content=prompt)]
        result = abot.graph.invoke({"messages": messages})
        print(result)

    gui.set_run_callback(callback_function)

    # run the agent
    gui.run()

if __name__ == "__main__":
    main()