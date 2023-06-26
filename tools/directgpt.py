import os
from langchain.agents import Tool
from dotenv import load_dotenv
import aiohttp
import requests
import json

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
load_dotenv(os.path.join(BASEDIR, '.env'), override=True)

def aoai(question):
        try:
            url = f"{str(os.getenv('OPENAI_API_BASE'))}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview"

            payload = json.dumps({
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ]
            })

            headers = {
            'api-key': str(os.getenv("OPENAI_API_KEY")),
            'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            response_json = response.json()

            print(response_json)

            return response_json["choices"][0]["message"]["content"]
                    
        except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"


async def async_aoai(question):
        try:
            url = f"{str(os.getenv('OPENAI_API_BASE'))}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview"

            payload = json.dumps({
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ]
            })

            headers = {
            'api-key': str(os.getenv("OPENAI_API_KEY")),
            'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, data=payload) as response:
                            response_json = await response.json()
                            
                            print(response_json)

                            return response_json["choices"][0]["message"]["content"]

        except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"



def AOAI():
    tools = []
    tools.append(Tool(
        name = "Direct call Azure OpenAI",
        func=aoai,
        description="Useful for when you need to answer questions using OpenAI. You must not amend user's question and input it as string directly.",
        return_direct=True
    ))
    return tools

def AAOAI():
    tools = []
    tools.append(Tool(
        name = "Direct call Azure OpenAI",
        func=aoai,
        description="Useful for when you need to answer questions using OpenAI. You must not amend user's question and input it as string directly.",
        coroutine=async_aoai,
        return_direct=True
    ))
    return tools

def directgpt():
    tools = []
    tools.extend(AAOAI())
    return tools