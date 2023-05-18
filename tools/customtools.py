from langchain.agents import Tool
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()

azchat=AzureChatOpenAI(
    client=None,
    openai_api_base=str(os.getenv("OPENAI_API_BASE")),
    openai_api_version="2023-03-15-preview",
    deployment_name=str(os.getenv("CHAT_DEPLOYMENT_NAME")),
    openai_api_key=str(os.getenv("OPENAI_API_KEY")),
    # openai_api_type = "azure"
)

prompt = PromptTemplate(
    input_variables=["ocrtext"],
    template="""What is the contact name? given the ocr text scanned mail from topleft to bottom right.
      {ocrtext}?""",
)

chain = LLMChain(llm=azchat, prompt=prompt)

class DocsInput(BaseModel):
    question: str = Field()


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

def FindName(input):
    result = chain.run(input)
    return result

def FindNameTool():
    tools = []
    tools.append(Tool(
        name = "Find Name",
        func=FindName,
        description=f"Useful for when you need to find a contact name from OCR text. Input should be a OCR text in text or JSON format. Output will be the contact name and it cannot be the final answer.",
        args_schema=DocsInput,
        return_direct=True
    ))
    return tools

def customtools():
    tools = []
    tools.extend(IDKTool())
    return tools