import streamlit as st  
import requests  
import os  
  
# Set subscription key and endpoint for Azure Cognitive Services API using environment variables  
subscription_key = os.environ['AZURE_COGNITIVE_SERVICES_KEY']  
endpoint = os.environ['AZURE_COGNITIVE_SERVICES_EP']  
  
# Set API endpoint for OCR service  
ocr_url = endpoint + "vision/v3.0/ocr"  
  
# Define function to upload image and perform OCR using Azure Cognitive Services API  
def ocr(image_file):  
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}  
    response = requests.post(ocr_url, headers=headers, data=image_file)  
    response.raise_for_status()  
    analysis = response.json()  
    return analysis  
  
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
