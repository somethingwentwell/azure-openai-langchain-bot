import os
import openai
from langchain.agents import Tool
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI
from langchain.agents import create_csv_agent
from pydantic import BaseModel, Field
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper

azllm=AzureOpenAI(deployment_name=os.getenv("COMPLETION_DEPLOYMENT_NAME"), model_name=os.getenv("COMPLETION_MODEL_NAME"), temperature=0)
load_dotenv()


class DocsInput(BaseModel):
    question: str = Field()

zapier = ZapierNLAWrapper()
zapier_toolkit = ZapierToolkit.from_zapier_nla_wrapper(zapier)
agent = initialize_agent(zapier_toolkit.get_tools(), azllm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def zapierAgent(input):
    response = agent.run(input)
    return response

def ZapierTool():
    tools = []
    tools.append(Tool(
        name = "Workflow Agent",
        func=zapierAgent,
        description=f"Useful for when you need to run workflow actions like email, trello cards etc. Input should be a question in complete sentence. Output will be the action result and you can use it as Final Answer.",
        args_schema=DocsInput
    ))
    return tools

def IDK(input):
    return "I don't know."

def IDKTool():
    tools = []
    tools.append(Tool(
        name = "IDK Agent",
        func=IDK,
        description=f"Useful for when you need to answer the questions that other tools cannot answer. Input should be a question in complete sentence. Output will be the action result and you can use it as Final Answer.",
        args_schema=DocsInput,
        return_direct=True
    ))
    return tools

def allCustomTools():
    tools = []
    tools.extend(IDKTool())
    return tools