from langchain.agents import Tool
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY") 
openai.api_version = "2023-07-01-preview"
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")

class DocsInput(BaseModel):
    question: str = Field()

functions= [
    {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA"
          },
          "unit": {
            "type": "string",
            "enum": ["celsius", "fahrenheit"]
          }
        },
        "required": ["location"]
      }
    }
]


def json_output(message):
    messages = [{
        "role": "user",
        "content": message
    }]
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo",
        messages=messages,
        functions=functions,
        function_call="auto", 
    )
    print(response)

    obj = {
        "content": response["choices"][0]["message"]["function_call"]["arguments"],
        "total_tokens": response["usage"]["total_tokens"]
    }

    return obj

def direct_json():
    tools = []
    tools.append(Tool(
        name = "JSON Formatter",
        func=json_output,
        description="Useful for when you need to answer questions using OpenAI. Input must be the exact same text as user's ask.",
        return_direct=True
    ))
    return tools


def azure_openai_functions():
    tools = []
    tools.extend(direct_json())
    return tools