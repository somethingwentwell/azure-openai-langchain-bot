import streamlit as st
import requests
import json
import time
from PIL import Image
from azure.storage.table import TableService

st.set_page_config(page_title="Shopping Mall", layout="wide", page_icon=":shopping_bags:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

table_service = TableService(account_name='insourcetable015', account_key='PVLQ/+Gkk1Qe8HBLbbAxz19jIbAxGEAiBWHpvIvufOJFR4Sb5UfQIEE4GTi3I8yhAVhyF8U+hyr3+AStN0E++w==')



# event1details = 

def query_table(partition_key):
    query = "PartitionKey eq '{}'".format(partition_key)
    entities = table_service.query_entities('mytable', filter=query)
    return entities

def insource_reply_shoplist(question ,shop_list):
    response_text = f"""
    You are an shopping mall customer service that help to reply consummer questions. You must follow the Rules below: 
    <Rules> 
    Rule 1: The reply must refer to the shoplist provided below. 
    Rule 2: Do not any question that not related to the shoplist below and reply 'I don't have information on this question'.
    Rule 3: If the question in Chinese, you must reply in Chinese.
    <Rules> 

    T & C: 
    {shop_list}

    Question from consummer:
    {question}
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": "2",  
      "text": response_text
    }
    response = requests.post(url, json=payload)  
    return response.json()

def insource_reply_event1(question ,eventdetails):
    response_text = f"""
    You are an shopping mall customer service that help to reply consummer questions. You must follow the Rules below: 
    <Rules> 
    Rule 1: The reply must refer to the event details provided below. 
    Rule 2: Do not any question that not related to the event details below and reply 'I don't have information on this question'.
    Rule 3: If the question in Chinese, you must reply in Chinese.
    <Rules> 

    T & C: 
    {eventdetails}

    Question from consummer:
    {question}
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": "2",  
      "text": response_text
    }
    response = requests.post(url, json=payload)  
    return response.json()

topics = ["Shop List", event1, event2]


partition_key = "shopping-mall-event"
shop_list = query_table(partition_key)
st.write(shop_list)
event1 = "The Point「會員狂賞節 – 任務」"

# image = Image.open("shopping_mall_banner.jpg")
# st.image(image, caption='Sunrise by the mountains')
st.write("Hello there! How can I assist you today?")
topic = st.selectbox("",topics)

def chatbot():
  # Initialize chat history
  if "messages" not in st.session_state:
      st.session_state.messages = []

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # Accept user input
  if question := st.chat_input("Enter enquiries"):
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": question})
      # Display user message in chat message container
      with st.chat_message("user"):
          st.markdown(question)

      # Display assistant response in chat message container
      with st.chat_message("assistant"):
          message_placeholder = st.empty()
          full_response = ""
          assistant_response = ""

          if topic == "Shop List":
             assistant_response = insource_reply_shoplist(question ,shop_list)['result']
          elif topic == event1 or topic == event2:
             assistant_response = insource_reply_event(question ,eventdetails)['result']

          # Simulate stream of response with milliseconds delay
          for chunk in assistant_response.split():
              full_response += chunk + " "
              time.sleep(0.05)
              # Add a blinking cursor to simulate typing
              message_placeholder.markdown(full_response + "▌")
          message_placeholder.markdown(full_response)
      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": full_response})

chatbot()