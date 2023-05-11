from fastapi import FastAPI, File, UploadFile, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from typing import List
import psycopg2
import os
import subprocess

app = FastAPI()

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

@app.post("/upload/{folder}/{subfolder}")
async def upload_file(folder: str, subfolder: str, file: UploadFile = File(...)):
    file_location = f"{folder}/{subfolder}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    return {"filename": file.filename}

@app.get("/read/{folder}/{subfolder}")
async def read_files(folder: str, subfolder: str):
    files = []
    for filename in os.listdir(f"{folder}/{subfolder}"):
        files.append(filename)
    return files

@app.get("/readall")
async def readall():
    files = []
    for filename in os.listdir("."):
        if os.path.isdir(filename) and filename in ["pdfs", "csvs", "htmls", "urls", "markdowns"]:
            files.append({filename: os.listdir(filename)})
    return {"files": files}

class DCActionReq(BaseModel):
    action: str

@app.post("/docker-compose")
async def docker_ps(req: DCActionReq):
    print(req)
    if req.action not in ["up", "down", "restart"]:
        return {"error": "Invalid action. Only 'up', 'down', and 'restart' are allowed."}
    try:
        result = subprocess.run(['docker-compose', req.action], stdout=subprocess.PIPE)
        print(result)
    except Exception as e:
        return {"error": str(e)}
    return {"result": result}



