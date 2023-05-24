import os
from langchain.agents import Tool
from dotenv import load_dotenv
from langchain.utilities import BingSearchAPIWrapper

search = BingSearchAPIWrapper()

def BingTool():
    tools = []
    tools.append(Tool(
        name = "search",
        func=search.run,
        description="useful for when you need to answer questions about current events"
    ))
    return tools

def bingsearchtool():
    tools = []
    tools.extend(BingTool())
    return tools