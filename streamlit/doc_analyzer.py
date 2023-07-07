import streamlit as st
import requests
import json
import os
import time
import random

st.set_page_config(page_title="Document Analyzer", page_icon=":page_facing_up:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Set subscription key and endpoint for Azure Cognitive Services API using environment variables  
subscription_key = os.environ['AZURE_COGNITIVE_SERVICES_KEY']  
endpoint = os.environ['AZURE_COGNITIVE_SERVICES_EP']  

# Set API endpoint for OCR service  
ocr_url = endpoint + "vision/v3.2/read/analyze"  


# Define function to perform OCR on uploaded file
def ocr_file(file):
    # Set up request headers and parameters
    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": subscription_key
    }
    params = {
        "language": "en",
        "detectOrientation": "true"
    }
    # Send request to Azure Cognitive Services API
    response = requests.post(ocr_url, headers=headers, params=params, data=file)

    # Wait Respond from Azure Cognitive Services API
    operation_url = response.headers["Operation-Location"]  
    response = requests.get(operation_url, headers=headers)  
    while response.json()["status"] != 'succeeded':  
        time.sleep(1)  
        response = requests.get(operation_url, headers=headers)
    #st.write(response.text)  	

    # Parse response JSON and extract OCR results
    response_json = json.loads(response.text)
    ocr_results = ""
    for region in response_json["analyzeResult"]["readResults"][0]["lines"]:
        for word in region["words"]:
            ocr_results += word["text"] + " "
        ocr_results += "\n"
    return ocr_results

def insource_summary(ocr_results):
    response_text = """
    Read the documnet provided and give a summary. 

    Document: 
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": 8502,  
      "text": response_text + "\n" + ocr_results
    }  
    response = requests.post(url, json=payload)
    return response.json()

def insource_insights(ocr_results):
    response_text = """
    Read the documnet provided and give some insights. 

    Document: 
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": 8502,  
      "text": response_text + "\n" + ocr_results
    }  
    response = requests.post(url, json=payload)
    return response.json()

def insource_chat(ocr_results, question):
    response_text = """
    Try your best to answer the question from user by using the document below. 

    Document: 
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": 8502,  
      "text": response_text + "\n" + ocr_results + "\n" + question
    }  
    response = requests.post(url, json=payload)
    return response.json()

def chatbot(ocr_results):
    st.write("Welcome! I'm a document analysis bot. You can upload a document and ask me anything about it. I'm here to assist you with any questions or concerns you may have. What can I help you with today?")

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
          assistant_response = insource_chat(ocr_results, question)['result']

          # Simulate stream of response with milliseconds delay
          for chunk in assistant_response.split():
             full_response += chunk + " "
             time.sleep(0.05)
          # Add a blinking cursor to simulate typing
             message_placeholder.markdown(full_response + "▌")
          message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Define Streamlit app
def app():
    st.sidebar.title("Document Analyzer")
    st.sidebar.write("Upload a PDF or image file to perform summarization.")
    placeholder = st.empty()
    actions = ["Summarization", "Chat with the Doc", "Bring Insights"]
    action = st.sidebar.selectbox("Perform", actions)
    # Allow user to upload file
    file = st.sidebar.file_uploader("Upload file", type=["pdf", "png", "jpg", "jpeg"])
    if file is not None and action == "Summarization":
        st.title("Document Summarization")
        # Perform OCR on uploaded file
        ocr_results = ocr_file(file.read())
        # Display OCR results
        #st.write("OCR Results: OK")
        #st.write(ocr_results)

        # Call InSource to get anylyst the OCR results  
        #st.write("InSource Response: OK")
        insource_response = insource_summary(ocr_results)['result']  
        st.write(insource_response)
    elif file is not None and action == "Chat with the Doc":
        # Perform OCR on uploaded file
        ocr_results = ocr_file(file.read())
        placeholder = chatbot(ocr_results)

    elif file is not None and action == "Bring Insights":
        st.title("Bring Insights (Preview)")
        # Perform OCR on uploaded file
        ocr_results = ocr_file(file.read())
        insource_response = insource_insights(ocr_results)['result']
        st.write(insource_response)
                
# Run Streamlit app
if __name__ == "__main__":
    app()