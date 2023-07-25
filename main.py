from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory, PostgresChatMessageHistory
from langchain.agents import initialize_agent, AgentType, AgentExecutor
from langchain.callbacks import tracing_enabled
from langchain.callbacks import get_openai_callback
from features.callback import CustomHandler, WSHandler
from dotenv import load_dotenv
from typing import Optional
import asyncio 
import os
import logging
import datetime
from tools.direct_gpt import aoai, async_aoai
from tools.azure_openai_functions import json_output
from agents.simple_memory_agent import SimpleMemoryAgent
from features.token_handler import log_token, get_token, get_total_tokens


#from tools.duckduckgo_search import duckduckgo_search
#from tools.python import python
#from tools.direct_gpt import direct_gpt
#from tools.azure_cognitive_services import azure_cognitive_services

# IMPORT TOOL START
#from tools.bing_search import bing_search
#from tools.shell import shell
#from tools.document_import import document_import
#from tools.chatgpt_plugins import chatgpt_plugins
#from tools.azure_openai_functions import azure_openai_functions
#from tools.aoai_on_data import aoai_on_data
#from tools.zapier import zapier
#from tools.image_analysis import image_analysis
#from tools.custom_tools import custom_tools
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

#tools.extend(duckduckgo_search())
#tools.extend(python())
#tools.extend(direct_gpt())
#tools.extend(azure_cognitive_services())

# ADD TOOL START 
#tools.extend(bing_search())
#tools.extend(shell())
#tools.extend(document_import(azchat))
#tools.extend(chatgpt_plugins())
#tools.extend(aoai_on_data())
#tools.extend(azure_openai_functions())
#tools.extend(zapier())
#tools.extend(image_analysis())
#tools.extend(custom_tools()) 
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
    "CUSTOM_AGENT": "custom_agent",
    "AOAI_FUNCTIONS": "aoai_functions",
}.get(agent_type_str, None)
if agent_type is None:
    raise ValueError(f"Invalid agent type: {agent_type_str}")

def SetupChatAgent(id, agent_type, callbacks):
    postgresUser = str(os.getenv("POSTGRES_USER"))
    postgresPassword = str(os.getenv("POSTGRES_PASSWORD"))
    postgresHost = str(os.getenv("POSTGRES_HOST"))
    postgresPort = str(os.getenv("POSTGRES_PORT"))
    history[id] = PostgresChatMessageHistory(
        connection_string=f"postgresql://{postgresUser}:{postgresPassword}@{postgresHost}:{postgresPort}/chat_history", 
        session_id=str(id))
    if (agent_type == "CUSTOM_AGENT"):
        memories[id] = ConversationSummaryBufferMemory(
            llm=azchat, 
            max_token_limit=2500, 
            memory_key="chat_history", 
            return_messages=True) 
        agent = SimpleMemoryAgent(
            tools=tools,
            llm=azchat)
        agent_chains[id] = AgentExecutor.from_agent_and_tools(
            agent=agent.setup(), 
            tools=tools, 
            memory=memories[id], 
            callbacks=callbacks,
            verbose=True, 
            handle_parsing_errors=True)
    if (agent_type == "OPENAI_FUNCTIONS" or agent_type == "OPENAI_MULTI_FUNCTIONS"):
        agent_chains[id] = initialize_agent(tools, azchat, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)
    elif (agent_type == "CHAT_CONVERSATIONAL_REACT_DESCRIPTION" or 
        agent_type == "CHAT_ZERO_SHOT_REACT_DESCRIPTION" or
        agent_type == "STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION"):
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
    agent_type: Optional[str] = str(os.getenv("AGENT_TYPE"))
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
async def run(msg: MessageReq):
    if (msg.id not in agent_chains):
        SetupChatAgent(msg.id, msg.agent_type, [CustomHandler(session_id=msg.id, user_q=msg.text)])
    try:
        total_tokens = 0
        with get_openai_callback() as cb:
            if (msg.agent_type == "DIRECT_GPT"):
                response_json = aoai(msg.text)
                response = response_json["content"]
                total_tokens = response_json["total_tokens"]
            elif (msg.agent_type == "AOAI_FUNCTIONS"):
                response_json = json_output(msg.text)
                response = response_json["content"]
                total_tokens = response_json["total_tokens"]
            elif (msg.agent_type == "CUSTOM_AGENT" or msg.agent_type == "OPENAI_FUNCTIONS" or msg.agent_type == "OPENAI_MULTI_FUNCTIONS"):
                response = agent_chains[msg.id].run(input=msg.text)
                total_tokens = cb.total_tokens
            else:
                response = agent_chains[msg.id].run(input="Your setting: " + str(os.getenv("CHAT_SYSTEM_PROMPT")) + "\nMe: " + msg.text + "\n")
                total_tokens = cb.total_tokens
                print("------MEMORY ID: " + msg.id + "-----")
                if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 2000):
                    clearMemory(msg.id)
                print("Conversation History: ")
                print(agent_chains[msg.id].memory.buffer)
                print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")
        log_token(msg.id, int(total_tokens), datetime.datetime.now())
    except Exception as e:
        response = str(e)
    history[msg.id].add_user_message(msg.text)
    history[msg.id].add_ai_message(response)
    result = MessageRes(result=response)
    return result

@app.post("/limit_run")
async def limit_run(msg: MessageReq):
    try:
        if (get_total_tokens() > int(str(os.getenv("TOTAL_TOKEN_LIMIT")))):
            return MessageRes(result="[ALERT] Total token limit reached. Please contact admin.")
        elif (get_token(msg.id) > int(str(os.getenv("TOTAL_TOKEN_LIMIT_PER_USER")))):
            return MessageRes(result="[ALERT] User token limit reached. Please contact admin.")
        else:
            return await run(msg)
    except Exception as e:
        print(e)
        return e
        # return "Please set TOTAL_TOKEN_LIMIT and TOTAL_TOKEN_LIMIT_PER_USER environment variables."

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        while True:
            try:
                total_tokens = 0
                with get_openai_callback() as cb:
                    msg = await websocket.receive_json()
                    msg = MessageReq(**msg)

                    if (msg.id not in agent_chains):
                        SetupChatAgent(msg.id, msg.agent_type, [WSHandler(websocket=websocket, session_id=msg.id, user_q=msg.text)])
                        await websocket.send_json({
                            "result": "Enabled Tools: " + str(tool_names)
                        }) 

                    if (msg.agent_type == "DIRECT_GPT"):
                        response_json = await asyncio.create_task(async_aoai(msg.text))
                        response = response_json["content"]
                        total_tokens = response_json["total_tokens"]
                    elif (msg.agent_type == "AOAI_FUNCTIONS"):
                        response_json = json_output(msg.text)
                        response = response_json["content"]
                        total_tokens = response_json["total_tokens"]
                    elif (msg.agent_type == "CUSTOM_AGENT"):
                        response = await asyncio.create_task(agent_chains[msg.id].arun(input=msg.text))
                        total_tokens = cb.total_tokens
                    else:
                        response = await asyncio.create_task(agent_chains[msg.id].arun(input="Your setting: " + str(os.getenv("CHAT_SYSTEM_PROMPT")) + "\nMe: " + msg.text + "\n"))
                        total_tokens = cb.total_tokens
                        print("------MEMORY ID: " + msg.id + "-----")
                        if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 2000):
                            clearMemory(msg.id)
                        print("Conversation History: ")
                        print(agent_chains[msg.id].memory.buffer)
                        print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")

                    history[msg.id].add_user_message(msg.text)
                    history[msg.id].add_ai_message(response)
                    log_token(msg.id, int(total_tokens), datetime.datetime.now())

                    await websocket.send_json({
                        "result": response
                        }) 
                    await websocket.send_json({
                        "result": "Used Tokens: " + str(total_tokens)
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



# RESTART: bc23c05b-ecac-4763-acc1-72ca0381b93a
