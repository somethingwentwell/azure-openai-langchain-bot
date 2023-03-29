from fastapi import FastAPI
from pydantic import BaseModel
from langchain import LLMChain
from langchain.llms import AzureOpenAI
from langchain.agents import initialize_agent, ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from docsimport import importedMarkdownTools, importedUrlTools, importedPdfTools, importedTxtTools
from dotenv import load_dotenv
import os

load_dotenv()

def SetupAgent(id):
    prefix = f"""{os.getenv("PROMPT_PREFIX")}
    You have access to the following tools:"""
    suffix = """Again, If the user ask you in Chinese, you MUST reply in Chinese. Begin!"

    {chat_history}
    Question: {input}
    {agent_scratchpad}"""

    prompt = ZeroShotAgent.create_prompt(
        tools, 
        prefix=prefix, 
        suffix=suffix, 
        input_variables=["input", "chat_history", "agent_scratchpad"]
    )
    print("-----PROMPT-----")
    print(prompt.template)
    memories[id] = ConversationBufferMemory(memory_key="chat_history")
    llm_chain = LLMChain(llm=azllm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
    agent_chains[id] = AgentExecutor.from_agent_and_tools(agent=agent, tools=tools, verbose=True, memory=memories[id], max_iterations=5, early_stopping_method="generate")

def Nothing(input):
    return

azllm=AzureOpenAI(deployment_name=os.getenv("COMPLETION_DEPLOYMENT_NAME"), model_name=os.getenv("COMPLETION_MODEL_NAME"), temperature=0)

memories = {}
agent_chains = {}
tools = [
    Tool(
        name = "none",
        func=Nothing,
        description="Just reply what you think"
    )
]

tools.extend(importedMarkdownTools(os.getenv("TOOLS_CATEGORY"), azllm))
tools.extend(importedUrlTools(os.getenv("TOOLS_CATEGORY"), azllm))
tools.extend(importedTxtTools(os.getenv("TOOLS_CATEGORY"), azllm))
tools.extend(importedPdfTools(os.getenv("TOOLS_CATEGORY"), azllm))

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
        SetupAgent(msg.id)
    result = MessageRes(result=agent_chains[msg.id].run(input=msg.text))

    return result


