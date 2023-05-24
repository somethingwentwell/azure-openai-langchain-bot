from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory, PostgresChatMessageHistory
from langchain.agents import initialize_agent, load_tools, AgentType
from callback import CustomHandler
from dotenv import load_dotenv
import os

# IMPORT TOOL START
#from tools.bingsearchtool import bingsearchtool
#from tools.duckduckgosearchtool import duckduckgosearchtool
#from tools.pythontool import pythontool
#from tools.docsimport import docsimport
#from tools.zapiertool import zapiertool
#from tools.customtools import customtools
# IMPORT TOOL END

load_dotenv()

memories = {}
history = {}
agents = {}
agent_chains = {}
# tools = []


azchat=AzureChatOpenAI(
    client=None,
    openai_api_base=str(os.getenv("OPENAI_API_BASE")),
    openai_api_version="2023-03-15-preview",
    deployment_name=str(os.getenv("CHAT_DEPLOYMENT_NAME")),
    openai_api_key=str(os.getenv("OPENAI_API_KEY")),
    # openai_api_type = "azure"
)
tools = load_tools(["llm-math"], llm=azchat)

# ADD TOOL START
#tools.extend(bingsearchtool())
#tools.extend(duckduckgosearchtool())
#tools.extend(pythontool())
#tools.extend(docsimport(os.getenv("TOOLS_CATEGORY"), azchat))
#tools.extend(zapiertool())
#tools.extend(customtools())
# ADD TOOL END

tool_names = [tool.name for tool in tools]

def SetupChatAgent(id):
    # memories[id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    postgresUser = str(os.getenv("POSTGRES_USER"))
    postgresPassword = str(os.getenv("POSTGRES_PASSWORD"))
    postgresHost = str(os.getenv("POSTGRES_HOST"))
    postgresPort = str(os.getenv("POSTGRES_PORT"))
    memories[id] = ConversationSummaryBufferMemory(
        llm=azchat, 
        max_token_limit=2500, 
        memory_key="chat_history", 
        return_messages=True)
    memories[id].save_context(
        {"input": os.getenv("CHAT_SYSTEM_PROMPT")}, 
        {"ouputs": "I will try my best to help for the upcoming questions."})
    history[id] = PostgresChatMessageHistory(
        connection_string=f"postgresql://{postgresUser}:{postgresPassword}@{postgresHost}:{postgresPort}/chat_history", 
        session_id=str(id))
    agent_chains[id] = initialize_agent(
        tools,
        azchat, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memories[id], 
        max_iterations=2, 
        early_stopping_method="generate",
        callbacks=[CustomHandler(session_id=id)])

    print(tools)


class MessageReq(BaseModel):
    id: str
    text: str

class MessageRes(BaseModel):
    result: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def keepAsking(mid, text):
    res = ""
    try:
        res = agent_chains[mid].run(input=text)
    except:
        res = keepAsking(mid, text)
    return res

def clearMemory(mid):
    newMessage = str(os.getenv("CHAT_SYSTEM_PROMPT")) + "\nThe summary as below:\n" + agent_chains[mid].memory.predict_new_summary(agent_chains[mid].memory.buffer, agent_chains[mid].memory.moving_summary_buffer)
    agent_chains[mid].memory.buffer.clear()
    agent_chains[mid].memory.save_context({"input": newMessage}, {"ouputs": "I will try my best to help for the upcoming questions."})

@app.post("/run")
def run(msg: MessageReq):
    if (msg.id not in agent_chains):
        SetupChatAgent(msg.id)
    # response = agent_chains[msg.id].run(input=msg.text)
    response = keepAsking(msg.id, msg.text)
    history[msg.id].add_user_message(msg.text)
    history[msg.id].add_ai_message(response)
    # clearMemory(msg.id)
    print("------MEMORY ID: " + msg.id + "-----")
    if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 2000):
        clearMemory(msg.id)
    print("Conversation History: ")
    print(agent_chains[msg.id].memory.buffer)
    print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")

    result = MessageRes(result=response)
    return result

@app.get("/tools")
def get_tools():
    tool_list = []
    for tool in tools:
        tool_dict = {"name": tool.name, "description": tool.description}
        tool_list.append(tool_dict)
    return {"tools": tool_list}
