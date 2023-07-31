import streamlit as st
import requests
import json
import os
import time
from pages.utils.style import add_style 
from pages.utils.gen_app import generated_app, create_app

add_style()

# Set subscription key and endpoint for Azure Cognitive Services API using environment variables  
subscription_key = os.environ['AZURE_COGS_KEY']  
endpoint = os.environ['AZURE_COGS_ENDPOINT']  

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

response_text = """
You are a JSON formatter tool that help on outputting JSON format form the input directly. 
Extract the following input into JSON format. 
<Rules>
Rule1: Do not use markdown in the output. 
Rule2: The final answer must be in JSON string like: 
{'Application Form': <For Public Rental Housing (PRH)>,
'Applicant': <Surname + Given Name>,
'Family Member 1': <Surname + Given Name>,
'Family Member 2': <Surname + Given Name>,
'Applicant DOB': <Day + Month + Year>,
'Family Member 1 DOB': <Day + Month + Year>,
'Family Member 2 DOB': <Day + Month + Year>,
'Applicant HKID': <H.K.I.C>,
'Family Member 1 HKID': <H.K.I.C>,
'Family Member 2 HKID': <H.K.I.C> } 
<Rules> 

JSON response as below: 
"""

def insource(ocr_results):
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": '8501_form',  
      "text": response_text + "\n" + ocr_results
    }  
    response = requests.post(url, json=payload)
    return response.json()

#def rephase_insource(response):
#    response1 = response.json()
#    response1 = json.dumps(response1)
#    start = response1.find('{', response1.find('{') + 1)
#    end = response1.rfind('}') - 1
#    new_response = response1[start:end]
#    new_response = new_response.replace("'", "\"")
#    return new_response

# Define Streamlit app
def app():
    st.title("Data Classification and Auto-filling")
    st.write("Upload a PDF or image file to perform data classification.")
    # Allow user to upload file
    file = st.file_uploader("Upload file", type=["pdf", "png", "jpg", "jpeg"])
    if file is not None:
        # Perform OCR on uploaded file
        ocr_results = ocr_file(file.read())
        # Display OCR results
        st.write("OCR Results:", ":heavy_check_mark:")
        #st.write(ocr_results)

        # Call InSource to get anylyst the OCR results
        insource_response = insource(ocr_results)['result']   
        st.write("InSource Response:", ":heavy_check_mark:")
        #st.write(insource_response)
 
        # Parse JSONL response into dictionary
        #new_response = rephase_insource(response)
        #st.write(parsed_obj)

        insource_response = insource_response.replace("'", "\"")
        result = json.loads(insource_response)
        for label, data in result.items():
          if isinstance(data, str):
            form = st.text_input(label, data)
          else:
            form = st.text_input(label, json.dumps(data))
        
# Run Streamlit app
if __name__ == "__main__":
    app()