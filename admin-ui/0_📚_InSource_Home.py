# create a streamlit page with sidebar about a dashboard with charts to postgres tables, below is the schema:    
# CREATE TABLE agent_log (    
#   id SERIAL PRIMARY KEY,    
#   session_id VARCHAR(255) NOT NULL,    
#   user_q VARCHAR(5000) NOT NULL,    
#   callback_type VARCHAR(255) NOT NULL,    
#   log JSON NOT NULL    
# );       
# CREATE TABLE token_count (    
#   id SERIAL PRIMARY KEY,    
#   session_id VARCHAR(255),    
#   timestamp TIMESTAMP NOT NULL,    
#   used_token NUMERIC NOT NULL    
# );  
# CREATE TABLE message_store (    
#   id SERIAL PRIMARY KEY,    
#   session_id VARCHAR(255),    
#   message JSON NOT NULL
# );  

import streamlit as st  
import psycopg2  
import pandas as pd  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt
import plotly.express as px  
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

# Fetch data from database  
def fetch_data(query):  
    conn = connect_to_db()  
    df = pd.read_sql(query, conn)  
    conn.close()  
    return df  

def fetch_message_store():  
    query = "SELECT * FROM message_store"  
    return fetch_data(query)  

def extract_messages(df):  
    messages = []  
    for index, row in df.iterrows():  
        message = row['message']['data']['content']  
        messages.append(message)  
    return ' '.join(messages)

def fetch_logs():  
    query = "SELECT log FROM agent_log"  
    return fetch_data(query)  

def generate_wordcloud(logs_df):  
    logs_text = " ".join(log["log"] for log in logs_df["log"])  
    wordcloud = WordCloud(background_color="white", max_words=100).generate(logs_text)  
    return wordcloud  

def daily_token_usage_per_month():  
    query = """  
    SELECT  
        date_trunc('month', timestamp) AS month,  
        date_trunc('day', timestamp) AS day,  
        SUM(used_token) AS daily_token_usage  
    FROM token_count  
    GROUP BY month, day  
    ORDER BY month, day  
    """  
    return fetch_data(query)  

def top_10_token_usage_id_per_month():  
    query = """  
    SELECT   
        session_id,  
        date_trunc('month', timestamp) AS month,  
        SUM(used_token) AS monthly_token_usage  
    FROM token_count  
    GROUP BY session_id, month  
    ORDER BY monthly_token_usage DESC, month  
    LIMIT 10  
    """  
    return fetch_data(query)  

st.title('InSource Dashboard') 
df = fetch_message_store()  
st.subheader('Word Cloud of Messages')  
messages = extract_messages(df)  
wordcloud = WordCloud(width=1920, height=400, background_color='white').generate(messages) 
plt.imshow(wordcloud, interpolation='bilinear')  
plt.axis("off")  
st.pyplot(plt.gcf())  

col1, col2 = st.columns([1, 1])

with col1:
    # st.subheader("Daily Token Usage per Month Chart")  
    daily_token_usage_df = daily_token_usage_per_month()  
    if not daily_token_usage_df.empty:  
        daily_token_usage_chart = px.line(  
            daily_token_usage_df,  
            x="day",  
            y="daily_token_usage",  
            color="month",  
            title="Daily Token Usage per Month",  
            labels={"month": "Month", "day": "Day"},  
        )  
        st.plotly_chart(daily_token_usage_chart)  
    else:  
        st.warning("No data found for daily token usage per month") 
 
with col2:
    st.subheader("Top 10 Token Usage ID per Month Table")  
    top_10_token_usage_df = top_10_token_usage_id_per_month()  
    if not top_10_token_usage_df.empty:  
        st.write(top_10_token_usage_df)  
    else:  
        st.warning("No data found for top 10 token usage id per month") 
