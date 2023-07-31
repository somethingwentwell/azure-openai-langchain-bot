import streamlit as st
import requests
import json
import time
import random
import os
from pages.utils.style import add_style 
from pages.utils.gen_app import generated_app, create_app

add_style()

def generate_job_ad(insource_response, default_requirements):
    ad = insource_response + "\n\n"
    ad += default_requirements
    return ad

def insource(jobtitle, requirements):
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": "2",  
      "text": f"I'm hiring for the position of {jobtitle} for XYZ Properties. Could you write a job description based on the template below by filling in items in [bracket]. /// [company name] Full Time - [Fill in Job title] Job Description [Fill in description of the company] Responsibilities: [Fill in suggested responsibilities] Requirements: {requirements} [Fill in additional suggested requirements] ///"  
    }
    response = requests.post(url, json=payload)  
    return response.json()

def insource_chat(job_ad, question):
    response_text = f"""
    Try your best to answer the modify the Job Ad based on user comment below. 

    Job Ad:
    {job_ad}

    User Comment: 
    {question}
    """
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": 8502,  
      "text": response_text
    }  
    response = requests.post(url, json=payload)
    return response.json()

def chatbot(job_ad):
    st.write("Welcome! I'm an AI Job Ad Creator. Feel free to let me know what you want to adjust for the Job Ad generated.")

    # Initialize chat history
    if "messages" not in st.session_state:
      st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
        st.markdown(message["content"])  

    if question:= st.chat_input("Enter your question here"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        # Display user message in chat message container
        with st.chat_message("user"):
          st.markdown(question)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
          message_placeholder = st.empty()
          full_response = ""
          new_job_ad = insource_chat(job_ad, question)['result']
          assistant_response = random.choice(
            [
                "Ok, here are the updated Job Ad.",
            ]
        )
          # Simulate stream of response with milliseconds delay
          for chunk in assistant_response.split():
             full_response += chunk + " "
             time.sleep(0.05)
          # Add a blinking cursor to simulate typing
             message_placeholder.markdown(full_response + "▌")
          message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        return new_job_ad

def app():
      st.title("Job Ad Creator")

      jobtitle = st.text_input("Enter job title:")
      requirements = st.text_area("Enter job requirements:")
      default_requirements = st.text_area("Enter default requirements:")

      job_ad = ""
      if st.button("Generate"):
          # Call InSource  
          insource_response = insource(jobtitle, requirements)['result']
          st.write("InSource Response:", ":heavy_check_mark:")

          job_ad = generate_job_ad(insource_response, default_requirements)
          st.text_area("Job Ad", value=job_ad, height=300)

app()
