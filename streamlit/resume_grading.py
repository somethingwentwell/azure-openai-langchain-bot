# Create a auto resume grading app using streamlit with the following:    
# 1. textbox to input requirements    
# 2. A table with Name, phone number, email, and description in 10 words, grading based on the requirements    
# 3. Upload file button to upload resume    
# 4. After uploaded resume, Azure OCR the resume and pass the OCR result to InSource API with the following JSON:
# {  
#   "id": "1",  
#   "text": "Extract Name, Phone Number, Email, Description, Grading based on the requirment with the OCR scanned text: <THE OCR RESULT>"  
# }  
# 5. Add InSource Response as a row to the table
# 6. Add a download button to download the table as csv file

import streamlit as st  
import pandas as pd  
import time  
import base64  

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def create_csv_download_link(df, filename="data.csv", text="Download CSV"):  
    csv = df.to_csv(index=False)  
    b64 = base64.b64encode(csv.encode()).decode()  
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'  
    return href  
  
  
st.title("Auto Resume Grading App")  
  
# Textbox to input requirements  
default_requirements = "Software engineer, Python, JavaScript, SQL, Git, Agile, REST API, problem-solving"  
requirements = st.text_area("Enter the job requirements:", value=default_requirements)  

# Upload file button to upload resume  
uploaded_file = st.file_uploader("Upload a resume", type=["pdf", "docx", "txt"])  
  
# Table to display the resumes  
columns = ["Name", "Phone Number", "Email", "Description", "Grade"]  
data = [  
    ["John Doe", "123-456-7890", "john.doe@example.com", "Software engineer with 5 years of experience", 7],  
    ["Jane Smith", "234-567-8901", "jane.smith@example.com", "Full-stack developer with 3 years of experience", 5],  
    ["Michael Brown", "345-678-9012", "michael.brown@example.com", "Data analyst with 4 years of experience", 6],  
    ["David Johnson", "567-890-1234", "david.johnson@example.com", "UX designer with 2 years of experience", 4],  
    ["Sophia Williams", "678-901-2345", "sophia.williams@example.com", "QA engineer with 6 years of experience", 7],  
    ["Daniel Jones", "789-012-3456", "daniel.jones@example.com", "DevOps engineer with 5 years of experience", 6],  
    ["Olivia Taylor", "890-123-4567", "olivia.taylor@example.com", "Technical writer with 3 years of experience", 5]  
]  
table = st.table(pd.DataFrame(data, columns=columns))  
  
  
if uploaded_file is not None:  
    # Read the uploaded file content  
    # resume_content = uploaded_file.read()  
  
    # Extract the necessary information from the resume  
    # You can use a library like PyPDF2 for PDFs or python-docx for Word documents  
    # For this example, let's assume you have extracted the following information:  
    name = "Stanley Leung"  
    phone_number = "852-5112-XXXX"  
    email = "stanley_xxxx@outlook.com"  
    description = "Security Guard with Cloud and Data Centre Administration Diploma"  

    time.sleep(4)  

    # Grade the resume based on the requirements  
    grade = 3
  
    # Add a row to the table  
    data.append([name, phone_number, email, description, grade])  
    table.table(pd.DataFrame(data, columns=columns))  


download_link = create_csv_download_link(pd.DataFrame(data, columns=columns))  
st.markdown(download_link, unsafe_allow_html=True)  