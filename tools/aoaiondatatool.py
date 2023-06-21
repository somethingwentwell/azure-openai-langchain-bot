import os
from langchain.agents import Tool
from dotenv import load_dotenv
import aiohttp
import requests
import json

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
load_dotenv(os.path.join(BASEDIR, '.env'), override=True)

def aoai_on_data_search(question):
        try:
            url = "https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/extensions/chat/completions?api-version=2023-06-01-preview"

            payload = json.dumps({
            "dataSources": [
                {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": str(os.getenv("AZURE_COGNITIVE_SEARCH_URL")),
                    "key": str(os.getenv("AZURE_COGNITIVE_SEARCH_KEY")),
                    "indexName": str(os.getenv("AZURE_COGNITIVE_SEARCH_INDEX_NAME"))
                }
                }
            ],
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ]
            })

            headers = {
            'api-key': str(os.getenv("OPENAI_API_KEY")),
            'chatgpt_url': 'https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-06-01-preview',
            'chatgpt_key': str(os.getenv("OPENAI_API_KEY")),
            'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            response_json = response.json()

            print(response_json)

            citations = json.loads(response_json["choices"][0]["messages"][0]["content"])["citations"]
            docs = ""
            i = 1
            for citation in citations:
                doc = f"<br>doc{str(i)} ({citation['filepath']}): <br>{citation['content'][:200]}...<br>"
                docs = docs + doc
                i = i + 1
            
            newOutput = f"{response_json['choices'][0]['messages'][1]['content']}<br><br>***Citations:*** {str(docs)}"

            return newOutput
                    
        except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"


async def async_aoai_on_data_search(question):
        try:
            url = "https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/extensions/chat/completions?api-version=2023-06-01-preview"

            payload = json.dumps({
            "dataSources": [
                {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": str(os.getenv("AZURE_COGNITIVE_SEARCH_URL")),
                    "key": str(os.getenv("AZURE_COGNITIVE_SEARCH_KEY")),
                    "indexName": str(os.getenv("AZURE_COGNITIVE_SEARCH_INDEX_NAME"))
                }
                }
            ],
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ]
            })

            headers = {
            'api-key': str(os.getenv("OPENAI_API_KEY")),
            'chatgpt_url': 'https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-06-01-preview',
            'chatgpt_key': str(os.getenv("OPENAI_API_KEY")),
            'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, data=payload) as response:
                            response_json = await response.json()
                            
                            print(response_json)

                            citations = json.loads(response_json["choices"][0]["messages"][0]["content"])["citations"]
                            docs = ""
                            i = 1
                            for citation in citations:
                                doc = f"<br>doc{str(i)} ({citation['filepath']}): <br>{citation['content'][:200]}...<br>"
                                docs = docs + doc
                                i = i + 1
                            
                            newOutput = f"{response_json['choices'][0]['messages'][1]['content']}<br><br>***Citations:*** {str(docs)}"


                            return newOutput
                    
        except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"



def AOAIDataSearch():
    tools = []
    tools.append(Tool(
        name = "Azure OpenAI on Data Search",
        func=aoai_on_data_search,
        description=str(os.getenv("AZURE_COGNITIVE_SEARCH_DESC")),
        return_direct=True
    ))
    return tools

def AAOAIDataSearch():
    tools = []
    tools.append(Tool(
        name = "Azure OpenAI on Data Search",
        func=aoai_on_data_search,
        description=str(os.getenv("AZURE_COGNITIVE_SEARCH_DESC")),
        coroutine=async_aoai_on_data_search,
        return_direct=True
    ))
    return tools

def aoaiondatatool():
    tools = []
    tools.extend(AAOAIDataSearch())
    return tools