from fastapi import FastAPI
from pydantic import BaseModel
from langchain import LLMChain
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import PostgresChatMessageHistory
from docsimport import allImportedTools
from customtools import allCustomTools
from dotenv import load_dotenv
import os
# os.environ["LANGCHAIN_HANDLER"] = "langchain"

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
history = {}
agents = {}
agent_chains = {}

tools = []
# tools.extend(allImportedTools(os.getenv("TOOLS_CATEGORY"), azllm))
tools.extend(allCustomTools())


tool_names = [tool.name for tool in tools]

def SetupChatAgent(id):
    # memories[id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    memories[id] = ConversationSummaryBufferMemory(llm=azchat, max_token_limit=1000, memory_key="chat_history", return_messages=True)
    memories[id].save_context({"input": os.getenv("CHAT_SYSTEM_PROMPT")}, {"ouputs": "I will try my best to help for the upcoming questions."})
    history[id] = PostgresChatMessageHistory(connection_string="postgresql://postgres:postgres@host.docker.internal:5432/chat_history", session_id=str(id))
    agent_chains[id] = initialize_agent(tools, azchat, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memories[id], max_iterations=5, early_stopping_method="generate")

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

def keepAsking(mid, text):
    res = ""
    try:
        res = agent_chains[mid].run(input=text)
    except:
        res = keepAsking(mid, text)
    return res

def clearMemory(mid):
    newMessage = os.getenv("CHAT_SYSTEM_PROMPT") + "\nThe summary as below:\n" + agent_chains[mid].memory.predict_new_summary(agent_chains[mid].memory.buffer, agent_chains[mid].memory.moving_summary_buffer)
    agent_chains[mid].memory.buffer.clear()
    agent_chains[mid].memory.save_context({"input": newMessage}, {"ouputs": "I will try my best to help for the upcoming questions."})

@app.post("/run")
def run(msg: MessageReq):
    if (msg.id not in agent_chains):
        SetupChatAgent(msg.id)
    response = agent_chains[msg.id].run(input=msg.text)
    history[msg.id].add_user_message(msg.text)
    history[msg.id].add_ai_message(response)
    # response = keepAsking(msg.id, msg.text)
    # clearMemory(msg.id)
    print("------MEMORY ID: " + msg.id + "-----")
    if (agent_chains[msg.id].memory.llm.get_num_tokens_from_messages(agent_chains[msg.id].memory.buffer) > 500):
        clearMemory(msg.id)
    print("Conversation History: ")
    print(agent_chains[msg.id].memory.buffer)
    print("------END OF MEMORY （" + str(len(agent_chains[msg.id].memory.buffer)) + ")-----")

    result = MessageRes(result=response)
    return result


