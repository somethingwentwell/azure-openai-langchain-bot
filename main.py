from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory, PostgresChatMessageHistory
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import tracing_enabled
from callback import CustomHandler, WSHandler
from dotenv import load_dotenv
import asyncio 
import os
import logging
from tools.directgpt import aoai, async_aoai

#from tools.duckduckgosearchtool import duckduckgosearchtool
#from tools.pythontool import pythontool
#from tools.directgpt import directgpt
#from tools.azurecognitiveservices import azurecognitiveservices

# IMPORT TOOL START
#from tools.bingsearchtool import bingsearchtool
#from tools.shelltool import shelltool
#from tools.docsimport import docsimport
#from tools.chatgptplugins import chatgptplugins
#from tools.aoaiondatatool import aoaiondatatool
#from tools.zapiertool import zapiertool
#from tools.customtools import customtools
# IMPORT TOOL END

load_dotenv(".env", override=True)

memories = {}
history = {}
agents = {}
agent_chains = {}
tools = []


azchat=AzureChatOpenAI(
    client=None,
    openai_api_base=str(os.getenv("OPENAI_API_BASE")),
    openai_api_version="2023-03-15-preview",
    deployment_name=str(os.getenv("CHAT_DEPLOYMENT_NAME")),
    openai_api_key=str(os.getenv("OPENAI_API_KEY")),
    # openai_api_type = "azure"
)
# tools = load_tools(["llm-math"], llm=azchat)

#tools.extend(duckduckgosearchtool())
#tools.extend(pythontool())
#tools.extend(directgpt())
#tools.extend(azurecognitiveservices())

# ADD TOOL START 
#tools.extend(bingsearchtool())
#tools.extend(shelltool())
#tools.extend(docsimport(azchat))
#tools.extend(chatgptplugins())
#tools.extend(aoaiondatatool())
#tools.extend(zapiertool())
#tools.extend(customtools()) 
# ADD TOOL END

tool_names = [tool.name for tool in tools]

agent_type_str = str(os.getenv("AGENT_TYPE"))
agent_type = {
    "CHAT_CONVERSATIONAL_REACT_DESCRIPTION": AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    "CHAT_ZERO_SHOT_REACT_DESCRIPTION": AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    "STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION": AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    "OPENAI_FUNCTIONS": AgentType.OPENAI_FUNCTIONS,
    "OPENAI_MULTI_FUNCTIONS": AgentType.OPENAI_MULTI_FUNCTIONS,
    "DIRECT_GPT": "direct_gpt",
}.get(agent_type_str, None)
if agent_type is None:
    raise ValueError(f"Invalid agent type: {agent_type_str}")

def SetupChatAgent(id, callbacks):
    postgresUser = str(os.getenv("POSTGRES_USER"))
    postgresPassword = str(os.getenv("POSTGRES_PASSWORD"))
    postgresHost = str(os.getenv("POSTGRES_HOST"))
    postgresPort = str(os.getenv("POSTGRES_PORT"))
    history[id] = PostgresChatMessageHistory(
        connection_string=f"postgresql://{postgresUser}:{postgresPassword}@{postgresHost}:{postgresPort}/chat_history", 
        session_id=str(id))
    if (str(os.getenv("AGENT_TYPE")) == "CHAT_CONVERSATIONAL_REACT_DESCRIPTION" or 
        str(os.getenv("AGENT_TYPE")) == "CHAT_ZERO_SHOT_REACT_DESCRIPTION" or
        str(os.getenv("AGENT_TYPE")) == "STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION"):
        memories[id] = ConversationSummaryBufferMemory(
            llm=azchat, 
            max_token_limit=2500, 
            memory_key="chat_history", 
            return_messages=True) 
        agent_chains[id] = initialize_agent(
            tools,
            azchat, 
            agent=agent_type,
            verbose=True, 
            memory=memories[id], 
            handle_parsing_errors=True,
            max_iterations=3, 
            early_stopping_method="generate",
            callbacks=callbacks)

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

def clearMemory(mid):
    newMessage = "\nThe chat history summary as below:\n" + agent_chains[mid].memory.predict_new_summary(agent_chains[mid].memory.buffer, agent_chains[mid].memory.moving_summary_buffer)
    agent_chains[mid].memory.buffer.clear()
    agent_chains[mid].memory.save_context({"input": newMessage}, {"ouputs": "OK, I will continue the conversation based on the chat history summary."})

@app.post("/run")
def run(msg: MessageReq):
    if (msg.id not in agent_chains):
        SetupChatAgent(msg.id, [CustomHandler(session_id=msg.id, user_q=msg.text)])
    if (str(os.getenv("AGENT_TYPE")) == "DIRECT_GPT"):
        response = aoai(msg.text)
    else:
        response = agent_chains[msg.id].run(input="Your setting: " + str(os.getenv("CHAT_SYSTEM_PROMPT")) + "\nMe: " + msg.text + "\n")
        # history[msg.id].add_user_message(msg.text)
        # history[msg.id].add_ai_message(response)
        print("------MEMORY ID: " + msg.id + "-----")
        if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 2000):
            clearMemory(msg.id)
        print("Conversation History: ")
        print(agent_chains[msg.id].memory.buffer)
        print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")
    history[msg.id].add_user_message(msg.text)
    history[msg.id].add_ai_message(response)
    result = MessageRes(result=response)
    return result

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            try:
                msg = await websocket.receive_json()
                msg = MessageReq(**msg)

                if (msg.id not in agent_chains):
                    SetupChatAgent(msg.id, [WSHandler(websocket=websocket, session_id=msg.id, user_q=msg.text)])
                    await websocket.send_json({
                        "result": "Enabled Tools: " + str(tool_names)
                    }) 

                if (str(os.getenv("AGENT_TYPE")) == "DIRECT_GPT"):
                    response = await asyncio.create_task(async_aoai(msg.text))
                else:
                    response = await asyncio.create_task(agent_chains[msg.id].arun(input="Your setting: " + str(os.getenv("CHAT_SYSTEM_PROMPT")) + "\nMe: " + msg.text + "\n"))
                    print("------MEMORY ID: " + msg.id + "-----")
                    if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 2000):
                        clearMemory(msg.id)
                    print("Conversation History: ")
                    print(agent_chains[msg.id].memory.buffer)
                    print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")

                history[msg.id].add_user_message(msg.text)
                history[msg.id].add_ai_message(response)

                await websocket.send_json({
                    "result": response
                    }) 
                
            except WebSocketDisconnect:
                logging.info("websocket disconnect")
                break
            except Exception as e:
                logging.error(e)
                await websocket.send_json({
                    "error": str(e)
                })

@app.get("/tools")
def get_tools():
    tool_list = []
    for tool in tools:
        tool_dict = {"name": tool.name, "description": tool.description}
        tool_list.append(tool_dict)
    return {"tools": tool_list}

# RESTART: 7ccef60c-35e9-423e-9a36-abe6addc06d3
