from langchain.agents import Tool
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
from langchain.utilities import PythonREPL
from langchain.chains import ConversationChain
from langchain.tools.file_management import (
    ReadFileTool,
    CopyFileTool,
    DeleteFileTool,
    MoveFileTool,
    WriteFileTool,
    ListDirectoryTool,
)
from langchain.agents.agent_toolkits import FileManagementToolkit
    
import requests
import json
import os

load_dotenv()

class DocsInput(BaseModel):
    question: str = Field()


def custom_tools():
    tools = []
    return tools