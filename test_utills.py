
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