import streamlit as st  
import requests  
import pandas as pd
import os
import json
import uuid
from pages.utils.style import add_style 
from pages.utils.gen_app import generated_app, create_app

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

edit, preview = st.columns([1,2])

with edit:

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["File Name", "Define Input", "Define Output", "Additional Requirements", "Confirm and Generate"])

    with tab1:
        appname = st.text_input("Enter your app name here (No space, no special character)")
        description = st.text_input("Enter your app description here")

    with tab2:
        stored_inputs = st.session_state.get("stored_inputs", [])  

        st.subheader("Add Inputs")
        new_input = st.text_input("Description of the input")
        input_type = st.radio("Select input type", ("Text", "Textarea", "Image", "PDF"))
        add_input = st.button("Add Input")  

        if add_input:  
            if new_input:  
                stored_inputs.append({"input": new_input, "type": input_type})  
                st.session_state["stored_inputs"] = stored_inputs  
            else:  
                st.warning("Empty input is not allowed")  

        st.divider()

        st.subheader("Input List")
        if stored_inputs:    
            col1, col2 = st.columns([1,1])
            for index, value in enumerate(stored_inputs):  
                row_text = f"{index + 1}. {value}" 
                with col1:
                    st.write(f"#### Input {index + 1}: {value['input']} ({value['type']})")
                with col2:
                    delete_button = st.button(f"Delete Input {index + 1}")  

                if delete_button:  
                    stored_inputs.pop(index)  
                    st.session_state["stored_inputs"] = stored_inputs  
                    st.experimental_rerun()  



    with tab3:
        stored_outputs = st.session_state.get("stored_outputs", [])   
        st.subheader("Add Outputs")
        new_output = st.text_input("Description of the output")
        output_type = st.radio("Select output type", ("Text", "Textarea"))
        add_output = st.button("Add Output") 

        if add_output:  
            if new_output:  
                stored_outputs.append({"output": new_output, "type": output_type})  
                st.session_state["stored_outputs"] = stored_outputs  
            else:  
                st.warning("Empty output is not allowed")  

        st.divider()

        st.subheader("Output List")
        if stored_outputs:  
            col1, col2 = st.columns([1,1])
            for index, value in enumerate(stored_outputs):  
                row_text = f"{index + 1}. {value}" 
                with col1:
                    st.write(f"#### Output {index + 1}: {value['output']} ({value['type']})")
                with col2:
                    delete_button_2 = st.button(f"Delete Output {index + 1}")  

                if delete_button_2:  
                    stored_outputs.pop(index)  
                    st.session_state["stored_outputs"] = stored_outputs  
                    st.experimental_rerun() 
    

    with tab4:
        additional_requirements = st.session_state.get("additional_requirements", "")   
        additional_requirements = st.text_area("Enter your additional additional requirements here (Optional)")
        if st.button("Add Additional Requirements"):
            st.session_state["additional_requirements"] = additional_requirements
            st.experimental_rerun()

    with tab5:
        st.write(f"App Name: {appname}")
        st.write(f"Description: {description}")
        if stored_inputs:  
            for index, value in enumerate(stored_inputs):  
                st.write(f"Input {index + 1}: {value['input']} ({value['type']})")
        if stored_outputs:  
            for index, value in enumerate(stored_outputs):  
                st.write(f"Output {index + 1}: {value['output']} ({value['type']})")
        st.write(f"Additional Requirements: {additional_requirements}")

        if st.button("Generate App"):
            if appname and stored_inputs and stored_outputs:
                create_app(appname, description, stored_inputs, stored_outputs, additional_requirements)
                st.success("Done! Check your app in the side bar.")
            else:
                st.warning("Please fill in all required fields before generating the app.")


with preview:
    st.subheader("Preview")
    generated_app(stored_inputs, stored_outputs, additional_requirements)