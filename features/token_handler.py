import decimal
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)
postgresUser = str(os.getenv("POSTGRES_USER"))
postgresPassword = str(os.getenv("POSTGRES_PASSWORD"))
postgresHost = str(os.getenv("POSTGRES_HOST"))
postgresPort = str(os.getenv("POSTGRES_PORT"))


def log_token(session_id: str, used_token: int, timestamp) -> None:
    conn = psycopg2.connect(
        host=postgresHost,
        port=postgresPort,
        database="chat_history",
        user=postgresUser,
        password=postgresPassword
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO token_count (session_id, used_token, timestamp) VALUES (%s, %s, %s)",
        (session_id, used_token, timestamp)
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
        "SELECT SUM(used_token)::int FROM token_count WHERE session_id = %s",
        (session_id,)
    )
    result = cur.fetchall()
    cur.close()
    conn.close()

    print(result)

    if result and result[0][0]:
        return int(result[0][0])
    else:
        return 0

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

    print(result)

    if result and result[0][0]:
        return int(result[0][0])
    else:
        return 0
