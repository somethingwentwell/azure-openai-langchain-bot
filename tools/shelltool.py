from langchain.agents import Tool
from pydantic import BaseModel, Field
from langchain.tools import ShellTool

class DocsInput(BaseModel):
    question: str = Field()

shell_tool = ShellTool()

shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace("{", "{{").replace("}", "}}")

def AShellTool():
    tools = []
    tools.append(Tool(
        name = "shell",
        func=shell_tool.run,
        coroutine=shell_tool.arun,
        description=shell_tool.description
    ))
    return tools

def shelltool():
    tools = []
    tools.extend(AShellTool())
    return tools