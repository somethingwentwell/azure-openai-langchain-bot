import streamlit as st
import requests
import json
import os
from pages.utils.style import add_style 
from pages.utils.gen_app import generated_app, create_app

add_style()

def insource_reply(complain):
    response_text = f"""
    You are an AI assistant that help user reply complain letter. You must follow the Rules below: 
    <Rules> 
    Rule 1: The suggested reply of the complain letter must in a {reply_tone} tone with at least 100 words 
    Rule 2: Your final answer is a complain letter reply with the answer of the customer questions.
    Rule 3: If customer ask in Chinese then the complain letter needs to respond in Chinese.
    <Rules> 

    Complain letter:
    """
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": "2",  
      "agent_type": "DIRECT_GPT",
      "text": response_text + complain  
    }
    response = requests.post(url, json=payload)  
    return response.json()

def insource_summary(complain):
    response_text = """
    You are an AI assistant that help on outputting JSON format for the input. Extract the following input into JSON format. The return should follow the format below: 
    {'Complain Service': '<Complain service>', 'Complain Branch': '<Complain branch>', 'Complain Person': '<complaining which staff>', 'Complain From': '<complain letter from who>'}
    Complain letter:
    """
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": "2",  
      "text": response_text + complain  
    }
    response = requests.post(url, json=payload)  
    return response.json()

st.title("Complaint Letter")

complain = st.text_area("Enter Complaint Letter:", height=200)

reply_tone = st.selectbox(
    "Reply Tone:",
    ("Professional", "Casual", "Enthusiastic", "Informational", "Funny")
)

if st.button("Generate"):
    # Call InSource
    insource_summary_response = insource_summary(complain)['result']  
    insource_reply_response = insource_reply(complain)['result']
    st.write("InSource Response:", ":heavy_check_mark:")

    # Dispaly Summary
    insource_summary_response = insource_summary_response.replace("'", "\"")
    result = json.loads(insource_summary_response)
    expander = st.expander("See Complaint Summary")
    with expander:
        for label, data in result.items():
            if isinstance(data, str):
                form = st.text_input(label, data)
        else:
            form = st.text_input(label, json.dumps(data))      

    # Dispaly Suggested Reply
    st.text_area("Suggested Reply:", value=insource_reply_response, height=600)

