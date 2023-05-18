from fastapi import FastAPI, File, UploadFile, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from dotenv import dotenv_values, set_key
import psycopg2
import os
import subprocess

app = FastAPI()
# Add middleware to add Access-Control-Allow-Origin header to all responses
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to the database
conn = psycopg2.connect(
    host="127.0.0.1",
    database="chat_history",
    user="postgres",
    password="postgres"
)

# Define the API endpoints
@app.get("/agent_log/{session_id}")
async def get_agent_logs(session_id: str) -> JSONResponse:
    cur = conn.cursor()
    cur.execute(f"SELECT callback_type, log FROM public.agent_log WHERE session_id='{session_id}'")
    rows = cur.fetchall()
    cur.close()
    return JSONResponse(content=rows)

@app.get("/message_store/{session_id}")
async def get_messages(session_id: str) -> JSONResponse:
    cur = conn.cursor()
    cur.execute(f"SELECT message FROM public.message_store WHERE session_id='{session_id}'")
    rows = cur.fetchall()
    cur.close()
    return JSONResponse(content=rows)

@app.get("/session_ids")
async def get_all_session_ids() -> JSONResponse:
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT session_id FROM public.message_store")
    rows = cur.fetchall()
    cur.close()
    session_ids = [row[0] for row in rows]
    return JSONResponse(content=session_ids)

@app.post("/upload/{folder}/{subfolder}")
async def upload_file(folder: str, subfolder: str, file: UploadFile = File(...)):
    file_location = f"./docs-data/{folder}/{subfolder}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}

@app.get("/read/{folder}/{subfolder}")
async def read_files(folder: str, subfolder: str):
    files = []
    for filename in os.listdir(f"./docs-data/{folder}/{subfolder}"):
        files.append(filename)
    return files

@app.get("/readall")
async def readall():
    files = []
    for filename in os.listdir("./docs-data"):
        if os.path.isdir(f"./docs-data/{filename}") and filename in ["txts", "pdfs", "csvs", "htmls", "urls", "markdowns"]:
            for subfolder in os.listdir(f"./docs-data/{filename}"):
                if os.path.isdir(f"./docs-data/{filename}/{subfolder}"):
                    files.append({"folder": filename, "subfolder": subfolder, "files": os.listdir(f"./docs-data/{filename}/{subfolder}")})
    return {"files": files}

class DCActionReq(BaseModel):
    action: str

@app.post("/service-ops")
async def docker_ps(req: DCActionReq):
    print(req)
    if req.action not in ["up", "down", "restart", "logs"]:
        return {"error": "Invalid action. Only 'up', 'down', and 'restart' are allowed."}
    try:
        result = subprocess.run(['docker-compose', req.action], stdout=subprocess.PIPE)
        print(result)
    except Exception as e:
        return {"error": str(e)}
    return {"result": result}

class ToolReq(BaseModel):
    name: str

@app.post("/toggle_tools")
async def toggle_tools(req: ToolReq):
    with open("main.py", "r") as f:
        lines = f.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if line.strip() == "# ADD TOOL START":
            start_index = i
        elif line.strip() == "# ADD TOOL END":
            end_index = i
        elif line.strip() == "# IMPORT TOOL START":
            import_start_index = i
        elif line.strip() == "# IMPORT TOOL END":
            import_end_index = i

    if start_index is None or end_index is None:
        return "Error: Could not find start and/or end of code block."

    for i in range(start_index + 1, end_index):
        if lines[i].startswith("#") and req.name in lines[i]:
            lines[i] = lines[i][1:]
        elif req.name in lines[i]:
            lines[i] = "#" + lines[i]

    if import_start_index is not None and import_end_index is not None:
        for i in range(import_start_index + 1, import_end_index):
            if lines[i].startswith("#") and req.name in lines[i]:
                lines[i] = lines[i][1:]
            elif req.name in lines[i]:
                lines[i] = "#" + lines[i]

    with open("main.py", "w") as f:
        f.writelines(lines)

    return "Code block toggled successfully."

@app.get("/disable_all_tools")
async def disable_tools():
    with open("main.py", "r") as f:
        lines = f.readlines()

    start_index = None
    end_index = None
    import_start_index = None
    import_end_index = None

    for i, line in enumerate(lines):
        if line.strip() == "# ADD TOOL START":
            start_index = i
        elif line.strip() == "# ADD TOOL END":
            end_index = i
        elif line.strip() == "# IMPORT TOOL START":
            import_start_index = i
        elif line.strip() == "# IMPORT TOOL END":
            import_end_index = i

    if start_index is None or end_index is None:
        return "Error: Could not find start and/or end of code block."

    for i in range(start_index + 1, end_index):
        if not lines[i].startswith("#"):
            lines[i] = "#" + lines[i]

    if import_start_index is not None and import_end_index is not None:
        for i in range(import_start_index + 1, import_end_index):
            if not lines[i].startswith("#"):
                lines[i] = "#" + lines[i]

    with open("main.py", "w") as f:
        f.writelines(lines)

    return "All tools disabled successfully."




@app.get("/toggle_tools")
async def get_toggle_tools():
    with open("main.py", "r") as f:
        lines = f.readlines()

    start_index = None
    end_index = None

    for i, line in enumerate(lines):
        if line.strip() == "# ADD TOOL START":
            start_index = i
        elif line.strip() == "# ADD TOOL END":
            end_index = i
        elif line.strip() == "# IMPORT TOOL START":
            import_start_index = i
        elif line.strip() == "# IMPORT TOOL END":
            import_end_index = i

    if start_index is None or end_index is None:
        return "Error: Could not find start and/or end of code block."

    tools = []

    for i in range(start_index + 1, end_index):
        if not lines[i].startswith("#"):
            tool = lines[i].strip().split("(")[1]
            tools.append(tool)

    return {"tools": tools}

@app.get("/env")
async def get_env() -> JSONResponse:
    env_vars = dotenv_values()
    return JSONResponse(content=env_vars)

class EnvReq(BaseModel):
    key: str
    value: str

@app.post("/env")
async def update_env(req: EnvReq) -> JSONResponse:
    env_vars = dotenv_values()
    if req.key not in env_vars:
        return JSONResponse(content={"error": f"Key '{req.key}' does not exist in env."})
    set_key(".env", req.key, req.value)
    env_vars = dotenv_values()
    return JSONResponse(content=env_vars)

@app.put("/env")
async def update_env(req: dict) -> JSONResponse:
    try:
        with open(".env", "w") as f:
            for key, value in req.items():
                f.write(f"{key}={value}\n")
        env_vars = dotenv_values()
        return JSONResponse(content=env_vars)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
