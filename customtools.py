import os
import openai
from langchain.agents import Tool
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI
from langchain.agents import create_csv_agent
from pydantic import BaseModel, Field

azllm=AzureOpenAI(deployment_name=os.getenv("COMPLETION_DEPLOYMENT_NAME"), model_name=os.getenv("COMPLETION_MODEL_NAME"), temperature=0)
load_dotenv()


class DocsInput(BaseModel):
    question: str = Field()

def libraryCsvTool():
    tools = []
    tools.append(Tool(
        name = "Book Searching Agent",
        func=csvAgent,
        description=f"useful for when you need to answer questions about the books and ACNO in Library. Input should be a question in complete sentence.",
        args_schema=DocsInput
    ))
    return tools

def csvAgent(input):
    agent = create_csv_agent(azllm, 'bookcsv/books.csv', verbose=True)
    response = agent.run(input)
    return response

def allCustomTools():
    tools = []
    # tools.extend(libraryCsvTool())
    return tools