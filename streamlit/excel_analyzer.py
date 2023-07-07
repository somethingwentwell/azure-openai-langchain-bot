import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title="Excel Analyzer", page_icon=":page_facing_up:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Define function to analyze data using ChatGPT and plot charts
def analyze_data(df):
    # Display data summary
    st.write("Data Summary:")
    st.write(df.describe())
    data = str(df.describe())

    # Use ChatGPT to generate insights
    insights = insource_summary(data)['result']
    st.write(insights)

    # # Plot histogram of data
    # st.write("Histogram:")
    # numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    # plt.hist(df[numeric_cols])
    # st.pyplot()

    # # Plot line chart of data
    # st.write("Line Chart:")
    # plt.plot(df)
    # st.pyplot()

def insource_summary(data):
    response_text = """
    Generate insights, summary, data relationship and prediction for this data: 
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
    "id": '8506',  
    "text": response_text + "\n" + data
    }  
    response = requests.post(url, json=payload)
    return response.json()

# Create page title and file uploader
st.title("Excel Analyzer")
file = st.file_uploader("Upload Excel file", type=["xlsx", "csv"])

# If file is uploaded, read data and analyze it
if file is not None:
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    st.write("Data:")
    st.write(df)
    analyze_data(df)
