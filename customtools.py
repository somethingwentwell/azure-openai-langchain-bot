import os
import openai
from langchain.agents import Tool
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI
from langchain.agents import create_csv_agent

load_dotenv()
azllm=AzureOpenAI(deployment_name=os.getenv("COMPLETION_DEPLOYMENT_NAME"), model_name=os.getenv("COMPLETION_MODEL_NAME"), temperature=0)

def custChatGPT(input):
    openai.api_type = "azure"
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_version = "2023-03-15-preview"
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        engine=os.getenv("CHAT_DEPLOYMENT_NAME"),
        messages = [{"role":"system","content":os.getenv("CHAT_SYSTEM_PROMPT")},
                    {"role":"user","content":input}],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    if response.choices[0].message.content:
        return response.choices[0].message.content
    return "Azure OpenAI Config Error"

def CustChatGPTTool():
    tools = []
    tools.append(Tool(
        name = "Custom ChatGPT Agent",
        func=custChatGPT,
        description=f"useful for when you need to answer questions about all the things that other tools can't answer. Input should be a question in complete sentence. "
    ))
    return tools

def libraryCsvTool():
    tools = []
    tools.append(Tool(
        name = "Book Searching Agent",
        func=csvAgent,
        description=f"useful for when you need to answer questions about the books in Library. Input should be a question in complete sentence."
    ))
    return tools


def csvAgent(input):
    agent = create_csv_agent(azllm, 'bookcsv/books.csv', verbose=True)
    preprompt = os.getenv("CSV_AGENT_PREPROMPT")
    response = agent.run(preprompt + input)
    return response


def allCustomTools():
    tools = []
    tools.extend(libraryCsvTool())
    tools.extend(CustChatGPTTool())
    return tools