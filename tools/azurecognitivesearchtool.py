import os
from langchain.agents import Tool
from dotenv import load_dotenv
from langchain.utilities import BingSearchAPIWrapper
import aiohttp

from langchain.retrievers import AzureCognitiveSearchRetriever

os.environ["AZURE_COGNITIVE_SEARCH_SERVICE_NAME"] = "warren-free-cognitive-search"
os.environ["AZURE_COGNITIVE_SEARCH_INDEX_NAME"] ="azureblob-index"
os.environ["AZURE_COGNITIVE_SEARCH_API_KEY"] = "pn3vwN2U9M5iGLNJ7Ku4V6rZ4cRQVGrXjVGTf0EjvdAzSeBmCMVK"

retriever = AzureCognitiveSearchRetriever(content_key="content")

async def search_acs(query):
    return retriever.get_relevant_documents(query)

def ACSTool():
    tools = []
    tools.append(Tool(
        name = "azure_cognitive_search",
        func=search_acs,
        coroutine=search_acs,
        description="useful for when you need to answer questions about internal data"
    ))
    return tools

def azurecognitivesearchtool():
    tools = []
    tools.extend(ACSTool())
    return tools