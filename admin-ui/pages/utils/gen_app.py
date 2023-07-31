import streamlit as st  
import fitz
import requests  
import json
import os
from PIL import Image
import io

template = """
import streamlit as st 
from pages.utils.gen_app import generated_app
from pages.utils.style import add_style 

add_style()

input = {stored_inputs}
output = {stored_outputs}
additional_requirements = "{additional_requirements}"
st.title("{appname}")
st.write("{description}")

generated_app(input, output, additional_requirements)
"""

def process_image(api_key, endpoint, image):  
    try:   
        headers = {  
            'Content-Type': 'application/octet-stream',  
            'Ocp-Apim-Subscription-Key': api_key  
        }  
        params = {  
            'detectOrientation': 'true',  
            'language': 'en'  
        }  
        ocr_ep = f"{endpoint}/vision/v3.2/ocr"
        response = requests.post(ocr_ep, headers=headers, params=params, data=image)  
  
        if response.status_code == 200:  
            ocr_result = json.loads(response.content)  
            return ocr_result  
        else:  
            st.write(f"Error processing image. Status code: {response.status_code}. Message: {response.text}")  
            return response.text  
    except Exception as e:  
        print(f"Error occurred: {str(e)}")  
        return e  

def format_ocr(image):
    ocr_result = process_image(os.getenv("AZURE_COGS_KEY"), os.getenv("AZURE_COGS_ENDPOINT"), image) 
    text = ""
    if ocr_result is not None:  
        for region in ocr_result["regions"]:
            for line in region["lines"]:
                for word in line["words"]:
                    text = text + " " + word["text"]
    return text

def pdf_to_images(pdf_data):  
    images = []  
    with fitz.open(stream=pdf_data, filetype="pdf") as doc:  
        for page in doc:  
            pix = page.get_pixmap(alpha=False)  
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  
            images.append(img)  
    return images  

def create_app(appname, description, stored_inputs, stored_outputs, additional_requirements):
    f = open(f"./pages/9_📲_App_-{appname}.py", "w")
    f.write(template.format(stored_inputs=stored_inputs, stored_outputs=stored_outputs, additional_requirements=additional_requirements, appname=appname, description=description))
    f.close()

def generated_app(stored_inputs, stored_outputs, additional_requirements):
    st.write(f"#### Input")
    inputs = stored_inputs

    if inputs:    
        for index, value in enumerate(inputs):  
            if (value['type'] == "Text"):
                value['value']  = st.text_input(f"{value['input']}")
            elif (value['type'] == "Textarea"):
                value['value'] = st.text_area(f"{value['input']}")
            else:
                if (value['type'] == "PDF"):
                    value['value'] = st.file_uploader("Choose a PDF file", type=["pdf"])
                    if value['value'] is not None:
                        value['value'] = pdf_to_images(value['value'].read())
                        text = ""
                        for i, image in enumerate(value['value'], 1): 
                            st.image(image, caption=f"Page {i}", use_column_width=False)
                            img_bytes = io.BytesIO()
                            image.save(img_bytes, format='PNG')
                            img_bytes = img_bytes.getvalue()
                            text += format_ocr(img_bytes)
                        value['value'] = text
                if (value['type'] == "Image"):  
                    value['value'] = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])  
                    if value['value'] is not None:
                        st.image(value['value'])
                        value['value'] = format_ocr(value['value'])



    # st.write(f"#### Output")
    outputs = stored_outputs

    if outputs:    
        for index, value in enumerate(outputs):  
            value['value'] = ""

    if st.button("Process"):
        prompt = '''

        {outputs}

        Given the outputs above. Try your best to fill the value with the follwing input and additional requirements (optional) as below:
        Input: {inputs}
        Additional Requirements: {additional_requirements}

        The desire output should be following the output above ONLY.
        '''

        formatted_text = prompt.format(additional_requirements=additional_requirements, inputs=inputs, outputs=outputs)
        # st.write(formatted_text)

        try:
            url = f"http://{os.getenv('INSOURCE_CHAT_HOST')}/run"
            payload = json.dumps(
                {
                "id": "app-test",
                "text": formatted_text
                }
            )

            response = requests.post(url, data=payload)
            response_json = response.json()
            content = response_json["result"]
            content = str(content).replace("'", '"')

            st.write(f"#### Output")
            outputs = json.loads(content)
            if outputs:    
                for index, value in enumerate(outputs):  
                    if (value['type'] == "Text"):
                        value['value']  = st.text_input(f"{value['output']}", value=value['value'])
                    if (value['type'] == "Textarea"):
                        value['value'] = st.text_area(f"{value['output']}", value=value['value'])
        
        except Exception as e:
            st.write(f"Error occurred, please try again.")  
            return e