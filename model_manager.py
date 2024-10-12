#directs the system to the correct cloud given the model selection

from groq import Groq
import os
from openai import OpenAI

openai_key = os.environ.get('OPENAI_KEY')

def identify_model(model):
    groq_models = set(
        ["distil-whisper-large-v3-en", "gemma2-9b-it", "gemma-7b-it", "llama3-groq-70b-8192-tool-use-preview",
         "llama3-groq-8b-8192-tool-use-preview", "llama-3.1-70b-versatile", "llama-3.1-8b-instant",
         "llama-3.2-1b-preview", "llama-3.2-3b-preview", "llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview",
         "llama-guard-3-8b", "llava-v1.5-7b-4096-preview", "llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768",
         "whisper-large-v3"])
    if model in groq_models:
        return "groq"
    open_IA_models = set(
        ["gpt-4o", "gpt-4o-2024-08-06", "gpt-4o-2024-05-13", "chatgpt-4o-latest", "gpt-4o-mini",
          "gpt-4o-mini-2024-07-18", "gpt-4o-mini", "gpt-4o-mini-2024-07-18", "o1-preview", "o1-preview-2024-09-12",
          "o1-mini", "o1-mini-2024-09-12", "gpt-4-turbo", "gpt-4-turbo-2024-04-09", "gpt-4-turbo-preview",
          "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4", "gpt-4-0613", "gpt-4-0314", "gpt-3.5-turbo-0125",
          "gpt-3.5-turbo", "gpt-3.5-turbo-1106","gpt-3.5-turbo-instruct"])

    if model in open_IA_models:
        return "open_ai"

def get_model_call(model = "llama3-groq-70b-8192-tool-use-preview"):
    """loads the needed api for the model"""
    model_provider = identify_model(model)

    if model_provider == "groq":
        groq_key = os.environ.get('GROQ_KEY')
        client = Groq(api_key=groq_key, )
        return client.chat.completions.create

    if model_provider == "open_ai":
        key = os.environ.get('OPENAI_KEY')
        client = OpenAI(api_key=key)
        return client.chat.completions.create

    print(f"Model {model} not found")
    assert False
    return None