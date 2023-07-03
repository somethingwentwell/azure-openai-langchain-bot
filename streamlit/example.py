# - Create a streamlit app that takes 3 inputs:                
# 1. English quiz type (grammar, vocab)                
# 2. Level (primary school 1-6)                
# 3. Number of questions                
            
# Create a submit button that puts these 3 input values to REST API post to http://localhost:8000/run with the following body format:                
# {                
#   "id": "1",                
#   "text": "Create <Number of questions><English quiz type> quizzes in level <Level>. You must reply me the questions and answers in markdown format."                
# }              
            
# - Show the response.result as markdown format  
# - Add a download button to download the markdown in streamlit

import requests  
import streamlit as st  
  
st.set_page_config(page_title="Streamlit Example")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


# Create inputs  
quiz_type = st.selectbox("Select quiz type", ["grammar", "vocab"])  
level = st.selectbox("Select level", ["Primary school 1", "Primary school 2", "Primary school 3", "Primary school 4", "Primary school 5", "Primary school 6"])  
num_questions = st.number_input("Number of questions", min_value=1, max_value=50, value=10)  
  
# Create submit button  
if st.button("Submit"):  
    # Create payload  
    payload = {  
        "id": "1",  
        "text": f"Create {num_questions} {quiz_type} quizzes in level {level}. You must reply me the questions and answers in markdown format."  
    }  
      
    # Post payload to REST API  
    response = requests.post("http://host.docker.internal:8000/run", json=payload)  
      
    # Show result  
    st.markdown(response.json()["result"])  
      
    # Add download button  
    st.download_button(  
        label="Download markdown",  
        data=response.json()["result"],  
        file_name="quiz.md",  
        mime="text/markdown",  
    )  
