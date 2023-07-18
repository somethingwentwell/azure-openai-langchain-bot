import streamlit as st  
import requests  
import pandas as pd
import os
import json
from pages.utils.style import add_style 

add_style()

def aoai(question):
        try:
            url = f"{str(os.getenv('OPENAI_API_BASE'))}/openai/deployments/gpt-35-turbo/chat/completions?api-version=2023-03-15-preview"
            payload = json.dumps({
            "messages": [
                {
                "role": "user",
                "content": question
                }
            ]
            })

            headers = {
            'api-key': str(os.getenv("OPENAI_API_KEY")),
            'Content-Type': 'application/json'
            }

            response = requests.post(url, headers=headers, data=payload)
            response_json = response.json()
            content = response_json["choices"][0]["message"]["content"]
            return content
                    
        except Exception as e:
                print(f"Error: {e}")
                return f"Error: {e}"


st.title("AI Web App Generator")  

appname = st.text_input("Enter your app name here (No space, no special character)")

objective = st.text_area("Enter your objective here")

input = st.text_area("Enter your App input here")

output = st.text_area("Enter your App expected output here")

prompt = '''
Draft a simple Streamlit app code which added the following code:
from pages.utils.style import add_style 
add_style()

The Streamlit app also need to fullfill the the following objective, input and desire output:

<OBJECTIVE-START>
{objective}
<OBJECTTIVE-END>

<INPUT-START>
{input}
<INPUT-END>

<DESIRE-OUTPUT-START>
{output}
<DESIRE-OUTPUT-END>

Click the "Submit" button to format the objective, input and desire output as text value to call the following API (Wrapped OpenAI API) to generate output:
path: http://{chat_host}/run
Request body: {{"id": "test","text": "<Formatted Text Value in string>"}}
The example response: {{"result": "<Response>"}}

Display the response in the app.
'''

if st.button("Submit"):
    formatted_text = prompt.format(objective=objective, input=input, output=output, chat_host=os.getenv("INSOURCE_CHAT_HOST"))
    response = aoai(formatted_text)
    # write response to file
    with open(f"./pages/_📲_{appname}_(AppTest).py", "w") as f:
        f.write(response.replace("```", ""))
    st.success("Done!")