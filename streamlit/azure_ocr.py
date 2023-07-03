# create a streamlit app with the following requirement:  
# 1. upload image or pdf then ocr the uploaded file using Azure cognitive service with python requests using environment variable AZURE_COGNITIVE_SERVICES_KEY and AZURE_COGNITIVE_SERVICES_EP  
# 2. After getting the OCR response, request http://localhost:8000/run with the following JSON {  
#   "id": "ws",  
#   "text": "Extract Date, From address, From phone number, To address, To phone number, order items, total from the OCR scanned text: <THE OCR RESULT>"  
# }  
# 3. Show the extracted text from the API response 

import streamlit as st  
import requests  
  
# Set subscription key and endpoint for Azure Cognitive Services API  
subscription_key = ""  
endpoint = "https://teccognitiveservices.cognitiveservices.azure.com/"  
  
# Set API endpoint for OCR service  
ocr_url = endpoint + "vision/v3.0/ocr"  
  
# Define function to upload image and perform OCR using Azure Cognitive Services API  
def ocr(image_file):  
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}  
    response = requests.post(ocr_url, headers=headers, data=image_file)  
    response.raise_for_status()  
    analysis = response.json()  
    return analysis  

def send_to_api(ocr_result):  
    url = "http://localhost:8000/run"  
  
    payload = {  
        "id": "ws",  
        "text": f'Extract Date, From address, From phone number, To address, To phone number, order items, total as markdown list from the OCR scanned text: "{ocr_result}"',  
    }  
  
    response = requests.post(url, json=payload)  
    response.raise_for_status()  
  
    return response.json()  
  
# Set up the Streamlit app  
st.title("OCR with Azure Cognitive Services")  
  
# Allow user to upload an image file  
image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])  
  
# Perform OCR and display the results  
if image_file is not None:  
    image_bytes = image_file.read()  
    result = ocr(image_bytes)  
    text = ""  
    for region in result['regions']:  
        for line in region['lines']:  
            for word in line['words']:  
                text += word['text'] + " "  
    st.header("OCR Result")  
    st.write(text)  
    api_response = send_to_api(text) 
    st.header("Extracted Text:")  
    st.write(api_response['result'])  
