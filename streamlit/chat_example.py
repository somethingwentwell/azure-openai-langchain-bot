# <REQUEST-START>

# curl --location --request POST 'https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview' \
# --header 'api-key: ' \
# --header 'Content-Type: application/json' \
# --data-raw '{
#     "messages": [
#         {
#             "role": "user",
#             "content": "Hi"
#         }
#     ]
# }'

# <REQUEST-END>

# <RESPONSE-START>

# {
#     "id": "chatcmpl-7Wfki1XrJ7ZqdGPSZuY9GjR3vfWJw",
#     "object": "chat.completion",
#     "created": 1688021348,
#     "model": "gpt-35-turbo",
#     "choices": [
#         {
#             "index": 0,
#             "finish_reason": "stop",
#             "message": {
#                 "role": "assistant",
#                 "content": "Hello! How can I assist you today?"
#             }
#         }
#     ],
#     "usage": {
#         "completion_tokens": 9,
#         "prompt_tokens": 9,
#         "total_tokens": 18
#     }
# }

# <RESPONSE-END>


# above is the azure openai chat API request and response, build a streamlit app using this API with a chat interface

import streamlit as st  
import requests  
import json  
  
st.set_page_config(page_title="Azure OpenAI Chat Assistant", page_icon=":speech_balloon:", layout="wide")  
  
st.title("Azure OpenAI Chat Assistant")  
  
def send_message_to_api(message):  
    url = 'https://tecopenai.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview'  
    headers = {  
        'api-key': '',  
        'Content-Type': 'application/json'  
    }  
    data = {  
        "messages": [  
            {  
                "role": "user",  
                "content": message  
            }  
        ]  
    }  
    response = requests.post(url, headers=headers, data=json.dumps(data))  
    return response.json()  
  
def process_response(response):  
    return response['choices'][0]['message']['content']  
  
user_input = st.text_input("Type your message here")  
submit_button = st.button("Send")  
  
if submit_button:  
    response = send_message_to_api(user_input)  
    ai_response = process_response(response)  
    st.write(f"Assistant: {ai_response}")  
