import json  
import requests  
from openapi_spec_validator import validate_spec 
import streamlit as st 
import os 
from pages.utils.style import add_style 

add_style()
  
def load_openapi_spec(url):  
    try:  
        response = requests.get(url)  
        response.raise_for_status()  
        spec = json.loads(response.text)  
        validate_spec(spec)  # Update this line  
        return spec  
    except Exception as e:  
        st.error(f"Error loading the OpenAPI specification: {str(e)}")  
        return None  

with st.sidebar:
    add_radio = st.radio(
        "Select API Endpoint",
        ("Admin", "Worker")
    )

spec_url = ""
title = ""
if add_radio == "Admin":
    title = "Admin API"
    spec_url = f"http://{os.getenv('INSOURCE_ADMIN_HOST')}" 
if add_radio == "Worker":
    title = "Worker API"
    spec_url = f"http://{os.getenv('INSOURCE_CHAT_HOST')}"
spec = load_openapi_spec(f"{spec_url}/openapi.json") 

if spec:  
    st.title(title)  
  
    for path, path_data in spec["paths"].items():  
        for method, method_data in path_data.items():  
            st.subheader(f"{method.upper()}: {spec_url}{path}")  
            st.write(f"Summary: {method_data['summary']}")
            st.write("Parameters:")  
            # Display parameters if any  
            # if "parameters" in method_data:  
            #     st.write("Parameters:")  
            #     for parameter in method_data["parameters"]:  
            #         st.write(f"- {parameter['name']} ({parameter['in']})")  

            # Create a form to test the API  
            with st.form(f"{path}_{method}"):  
                # Collect input for each parameter  
                inputs = {}  
                if "parameters" in method_data:  
                    for parameter in method_data["parameters"]:  
                        if parameter["in"] == "path":  
                            inputs[parameter["name"]] = st.text_input(f"{parameter['name']} (path)", "")  
                        elif parameter["in"] == "query":  
                            inputs[parameter["name"]] = st.text_input(f"{parameter['name']} (query)", "")  
  
                # Send request on form submission  
                if st.form_submit_button("Send Request"):  
                    url = f"{spec_url}{path.format(**inputs)}"  
                    response = requests.request(method, url, params=inputs)  
  
                    # Display response  
                    st.write(f"Status Code: {response.status_code}")  
                    st.write("Response JSON:")  
                    st.json(response.text)  

