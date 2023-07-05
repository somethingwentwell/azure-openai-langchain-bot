import decimal
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)
postgresUser = str(os.getenv("POSTGRES_USER"))
postgresPassword = str(os.getenv("POSTGRES_PASSWORD"))
postgresHost = str(os.getenv("POSTGRES_HOST"))
postgresPort = str(os.getenv("POSTGRES_PORT"))


def log_token(session_id: str, used_token: int) -> None:
    conn = psycopg2.connect(
        host=postgresHost,
        port=postgresPort,
        database="chat_history",
        user=postgresUser,
        password=postgresPassword
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO token_count (session_id, used_token) VALUES (%s, %s) ON CONFLICT (session_id) DO UPDATE SET used_token = token_count.used_token + %s",
        (session_id, used_token, used_token)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_token(session_id: str) -> int:
    conn = psycopg2.connect(
        host=postgresHost,
        port=postgresPort,
        database="chat_history",
        user=postgresUser,
        password=postgresPassword
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT used_token::int FROM token_count WHERE session_id = %s",
        (session_id,)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()

    return int(str(result[0][0])) if result else 0

def get_total_tokens() -> int:
    conn = psycopg2.connect(
        host=postgresHost,
        port=postgresPort,
        database="chat_history",
        user=postgresUser,
        password=postgresPassword
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT SUM(used_token)::int FROM public.token_count"
    )
    result = cur.fetchall()
    cur.close()
    conn.close()

    return int(str(result[0][0])) if result else 0
