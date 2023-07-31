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
    query = "SELECT DISTINCT session_id FROM message_store;"  
    df = pd.read_sql_query(query, conn)  
    return df['session_id'].tolist()  
  
# Function to fetch chat history by session_id  
def get_chat_history(session_id, conn):  
    query = f"SELECT * FROM message_store WHERE session_id = '{session_id}';"  
    df = pd.read_sql_query(query, conn)  
    return df  

# Function to display chat history like a dialogue  
def display_chat_history(chat_history):  
    for index, row in chat_history.iterrows():  
        message = row['message']
        content = message['data']['content']  
        msg_type = message['type']  
  
        # with st.chat_message("user"):
        #     if msg_type == 'human':  
        #         st.write(content)
        #         st.write(f"User: {content}") 
        # with st.chat_message("assistant"):
        #     if msg_type == 'ai':  
        #         st.write(content)
        #         st.write(f"AI: {content}") 
        if msg_type == 'human':  
            msg = st.chat_message("user")
            msg.write(f"User: {content}")  
        else:  
            msg = st.chat_message("assistant")
            msg.write(f"AI: {content}")  
  
# Main Streamlit app  
def main():  
    st.sidebar.title("History")  
  
    conn = connect_to_db()  
    session_ids = get_session_ids(conn)  
    selected_session_id = st.sidebar.selectbox("Select session_id", session_ids)  
  
    st.title(f"History for session_id: {selected_session_id}")  
  
    chat_history = get_chat_history(selected_session_id, conn)  
    display_chat_history(chat_history)  
  
    conn.close()  
  
if __name__ == "__main__":  
    main()  