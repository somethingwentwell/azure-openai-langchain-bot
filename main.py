from fastapi import FastAPI
from pydantic import BaseModel
from langchain import LLMChain
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from docsimport import allImportedTools
from customtools import allCustomTools
from dotenv import load_dotenv
import os
os.environ["LANGCHAIN_HANDLER"] = "langchain"

load_dotenv()

azllm=AzureOpenAI(deployment_name=os.getenv("COMPLETION_DEPLOYMENT_NAME"), model_name=os.getenv("COMPLETION_MODEL_NAME"), temperature=0)
azchat=AzureChatOpenAI(
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    openai_api_version="2023-03-15-preview",
    deployment_name=os.getenv("CHAT_DEPLOYMENT_NAME"),
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_type = "azure",
)

memories = {}
agents = {}
agent_chains = {}

tools = []
tools.extend(allImportedTools(os.getenv("TOOLS_CATEGORY"), azllm))
tools.extend(allCustomTools())


tool_names = [tool.name for tool in tools]

def SetupChatAgent(id):
    # memories[id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memories[id] = ConversationSummaryBufferMemory(llm=azchat, max_token_limit=50, memory_key="chat_history", return_messages=True)
    memories[id].save_context({"input": os.getenv("CHAT_SYSTEM_PROMPT")}, {"ouputs": "Copy that"})
    
    agent_chains[id] = initialize_agent(tools, azchat, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memories[id], max_iterations=2, early_stopping_method="generate")

# loop tools descriptions
print("-----TOOLS-----")
for tool in tools:
    print("[NAME] " + tool.name)
    print("[DESC] " + tool.description)
    print("")


print("-----READY-----")

class MessageReq(BaseModel):
    id: str
    text: str

class MessageRes(BaseModel):
    result: str

app = FastAPI()

@app.post("/run")
def run(msg: MessageReq):
    if (msg.id not in agent_chains):
        SetupChatAgent(msg.id)
    response = agent_chains[msg.id].run(input=msg.text)
    print("------MEMORY ID: " + msg.id + "-----")
    print("Conversation History: ")
    print(agent_chains[msg.id].memory.buffer)
    print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")
    result = MessageRes(result=response)
    return result


