import streamlit as st
import requests
import json
from streamlit_elements import elements, mui, html, dashboard

def insource_gen_prompt(prompt):
    response_text = """
    You are an assistant to help to generate a perfect prompt for generating an image.  
    The final answer must be in JSON string like: 
    {'question': <improve the prompt by asking user a question>, 'choice1': <choice1>, 'choice2': <choice2>, 'choice3': <choice3>, 'choice4': <choice4>}

    User input: 
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": 8502,  
      "text": response_text + "\n" + prompt
    }  
    response = requests.post(url, json=payload)
    return response.json()

# Define Streamlit app
def app():
    st.title("Image Prompt Generator")
    st.write("This app generates a prompt for an image based on user input.")
    
    user_prompt =""
    
    prompt = st.text_input("Enter a prompt:", user_prompt)
    if st.button("Generate"):
        insource_response = insource_gen_prompt(prompt)['result']
        prompt = insource_response.replace("'", "\"")
        prompt = json.loads(prompt)
        st.write(prompt['question'])

        if st.button(prompt['choice1']):    
            user_prompt = user_prompt + prompt['choice1']
        if st.button(prompt['choice2']):    
            user_prompt = user_prompt + prompt['choice2']
        if st.button(prompt['choice3']):    
            user_prompt = user_prompt + prompt['choice3']    

if __name__ == "__main__":
    app()