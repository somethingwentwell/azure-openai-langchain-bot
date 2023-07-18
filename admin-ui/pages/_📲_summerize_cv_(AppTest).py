import streamlit as st
import requests

st.set_page_config(
    page_title="InSource",
    page_icon="📚",
    layout="wide"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.write("# CV Summarization App")

input_text = st.text_area("Please input your CV:")

if st.button("Submit"):
    # formatting input text
    formatted_text = f"<OBJECTIVE-START>\nPlease help to summarize the CV with below major categories in max of 30 words on each. Personal info, Technical Skill, Experience\n<OBJECTTIVE-END>\n\n<INPUT-START>\n{input_text}\n<INPUT-END>\n\n<DESIRE-OUTPUT-START>\nPersonal Info\n[Sex]; [Age]; [Address]\n\nTechnical Skill\n[Summarize Technical Skill from CV]\n\nExperience\n[Summarize the Experience for each job from CV with Company Name; Present by number of years]\n<DESIRE-OUTPUT-END>"
    
    # calling OpenAI API
    url = "http://host.docker.internal:8000/run"
    data = {"id": "test","text": formatted_text}
    response = requests.post(url, json=data).json()
    
    # displaying result
    st.write("## Result")
    st.write(response["result"])