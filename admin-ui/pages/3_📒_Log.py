import streamlit as st  
import psycopg2  
import pandas as pd   
import os
from pages.utils.style import add_style 

add_style()
  
# Database connection  
def connect_to_db():  
    return psycopg2.connect(
        host=str(os.getenv("POSTGRES_HOST")),
        database="chat_history",
        user=str(os.getenv("POSTGRES_USER")),
        password=str(os.getenv("POSTGRES_PASSWORD"))
    )
    

# Function to fetch all session_ids  
def get_session_ids(conn):  
    query = "SELECT DISTINCT session_id FROM agent_log;"  
    df = pd.read_sql_query(query, conn)  
    return df['session_id'].tolist()  
  
# Function to fetch chat history by session_id  
def get_agent_log(session_id, conn):  
    query = f"SELECT id, session_id, user_q, callback_type, CAST(log AS TEXT) FROM agent_log WHERE session_id = '{session_id}';"  
    df = pd.read_sql_query(query, conn)  
    return df  
  
# Main Streamlit app  
def main():  
    st.sidebar.title("Log")
  
    conn = connect_to_db()  
    session_ids = get_session_ids(conn)  
    selected_session_id = st.sidebar.selectbox("Select session_id", session_ids)  
  
    st.title(f"Log for session_id: {selected_session_id}")  
  
    chat_history = get_agent_log(selected_session_id, conn)  
    st.write(chat_history)  
  
    conn.close()  
  
if __name__ == "__main__":      main()

