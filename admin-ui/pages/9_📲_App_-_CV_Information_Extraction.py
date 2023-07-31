
import streamlit as st 
from pages.utils.gen_app import generated_app
from pages.utils.style import add_style 
from pages.utils.gen_app import generated_app, create_app

add_style()

input = [{'input': 'Resume', 'type': 'PDF', 'value': None}]
output = [{'output': 'Name', 'type': 'Text', 'value': ''}, {'output': 'Skills', 'type': 'Text', 'value': ''}]
additional_requirements = "Skills should be less than 3."
st.title("cv")
st.write("")

generated_app(input, output, additional_requirements)
