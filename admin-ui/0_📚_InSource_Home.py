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
import requests
import json
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
    query = "SELECT message FROM message_store ORDER BY id DESC LIMIT 100"  
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

def daily_request_per_month():  
    query = """  
    SELECT  
        date_trunc('month', timestamp) AS month,  
        date_trunc('day', timestamp) AS day,  
        COUNT(*) AS daily_request  
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

def query_adminapi_all_token_used(range_type):
    API_ENDPOINT = "http://insource-test-015.southeastasia.cloudapp.azure.com:8100/all_token_used/"
    response = requests.get(API_ENDPOINT + range_type)
    data = json.loads(response.text)
    return data

st.subheader('| TOKEN USAGE')

col1, col2, col3, col4 = st.columns(4)
# column 1
with col1:
    range_type = "year"
    year_total = query_adminapi_all_token_used(range_type)["all_token_used"]
    st.title(year_total)
    st.text('THIS YEAR')
# column 2
with col2:
    range_type = "month"
    month_total = query_adminapi_all_token_used(range_type)["all_token_used"]
    st.title(month_total)
    st.text('THIS MONTH')
# column 3
with col3:
    range_type = "day"
    today_total = query_adminapi_all_token_used(range_type)["all_token_used"]
    st.title(today_total)
    st.text('TODAY')
# column 4
with col4:
    st.title(55)
    st.text('CLIENTS')

daily_token_usage_df = daily_token_usage_per_month()  
daily_request_df = daily_request_per_month()
chart_data = pd.merge(daily_token_usage_df, daily_request_df, on="day")
if not daily_token_usage_df.empty: 
    col1, col2 = st.columns((1,1)) 
    with col1: 
        st.subheader('| DAILY TOKEN USAGE')
        st.line_chart(  
            daily_token_usage_df,  
            x="day",  
            y="daily_token_usage",
            use_container_width = True  
        )  
    with col2: 
        st.subheader('| DAILY REQUEST')   
        st.line_chart(  
            daily_request_df,  
            x="day",  
            y="daily_request",  
            use_container_width = True 
        )  
else:  
    st.warning("No data found for daily token usage per month") 

col1, col2, col3 = st.columns((1,1,1))  

with col1: 
    st.subheader("Top 10 Token Usage ID per Month")
    top_10_token_usage_df = top_10_token_usage_id_per_month()  
    if not top_10_token_usage_df.empty:  
        # Create a pie chart
        fig, ax = plt.subplots()
        ax.pie(top_10_token_usage_df['monthly_token_usage'], labels=top_10_token_usage_df['session_id'], autopct='%1.1f%%')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig)
    else:  
        st.warning("No data found for top 10 token usage id per month")
with col2:
    st.subheader("Top 10 Token Usage ID per Month Table")  
    top_10_token_usage_df = top_10_token_usage_id_per_month()  
    if not top_10_token_usage_df.empty:  
        st.write(top_10_token_usage_df)  
    else:  
        st.warning("No data found for top 10 token usage id per month") 

with col3:
    df = fetch_message_store()
    st.subheader('Word Cloud of Messages')     
    messages = extract_messages(df)  
    wordcloud = WordCloud(width=800, height=600, background_color='white').generate(messages) 
    plt.imshow(wordcloud, interpolation='bilinear')  
    plt.axis("off")  
    st.pyplot(plt.gcf())