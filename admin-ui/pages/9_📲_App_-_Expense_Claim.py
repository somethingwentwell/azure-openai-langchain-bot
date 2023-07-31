import streamlit as st
import requests
import json
import os
import time
import pandas as pd
import base64
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
{'customer': <Leave in blank to customer fill up>,
'merchants': <Classify the Shop name on the receipt>,
'date': <DD-MM-YYYY>,
'type_of_claim': <Entertainment, Transportation, Phone, Outport, Medical>,
'total_amount_hkd': <Classify and report the total sum on receipt, return in integrate>, 
'cost_centre': <1001>} 
<Rules> 
JSON response as below: 
"""

def insource(ocr_results):
    url = f"http://{str(os.getenv('INSOURCE_CHAT_HOST'))}/run"  
    payload = {  
      "id": '8501_nwc',  
      "text": response_text + "\n" + ocr_results
    }  
    response = requests.post(url, json=payload)
    return response.json()

def create_csv_download_link(df, filename="data.csv", text="Download CSV"):  
    csv = df.to_csv(index=False)  
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'  
    return href  

# Define Streamlit app
def app():
    st.title("Expense Claim")
    st.write("Upload a PDF or image file to perform data classification.")
    # Allow user to upload file
    files = st.file_uploader("Upload file", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if files:
        # Initialize empty list to store results
        data = []
        columns = ["Customer", "Merchants", "Date", "Type of Claim", "Total Amount (HKD)", "Cost Centre"]
        # table = st.table(pd.DataFrame(data, columns=columns))
        # Loop through uploaded files
        for file in files:
            # Perform OCR on uploaded file    
            ocr_results = ocr_file(file.read())
            # Display OCR results
            st.write("OCR Results:", ":heavy_check_mark:")

            # Call InSource to get anylyst the OCR results
            insource_response = insource(ocr_results)['result']   
            st.write("InSource Response:", ":heavy_check_mark:")
 
            try:    
                # Parse JSONL response into dictionary
                # new_response = rephase_insource(response)
                # st.write(parsed_obj)

                insource_response = insource_response.replace("'", "\"")
                result = json.loads(insource_response)
                st.write(result)
            
                customer = result['customer']
                merchants = result['merchants']
                date = result['date']
                type_of_claim = result['type_of_claim']
                total_amount_hkd = result['total_amount_hkd']
                cost_centre = result['cost_centre']
                # st.write(customer)
                # st.write(merchants)
                # st.write(date)

                # Creat dataframe form result and append to list
                data.append([customer, merchants, date, type_of_claim, total_amount_hkd, cost_centre])  
                # table.table(pd.DataFrame(data, columns=columns)) 

            except json.JSONDecodeError as e:
                st.write("Error decoding JSON:", e)

        st.data_editor(pd.DataFrame(data, columns=columns))  

        # Download Link from DataFrame
        download_link = create_csv_download_link(pd.DataFrame(data, columns=columns))  
        st.markdown(download_link, unsafe_allow_html=True) 
                

# Run Streamlit app
if __name__ == "__main__":
    app()