# this is an openapi spec for http://localhost:8100/, create a streamlit config page to let user to read and edit env with nice looking UI components
import streamlit as st  
import requests  
import pandas as pd
import os

st.set_page_config(
    page_title="InSource",
    page_icon="📚",
    layout="wide"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

st.title("Configuration")  

with st.sidebar:
    add_radio = st.radio(
        "Select Configuration",
        ("Server Status", "Environment Variables", "Tools", "Document Upload")
    )
  
API_URL = f"http://{os.getenv('INSOURCE_ADMIN_HOST')}"  

if add_radio == "Server Status":
    # Create a function to check server status  
    def check_server_status(url):  
        response = requests.post(f"{API_URL}/chat_server_status", json={"url": url})  
        return response.json()  
    
    # Create a function to restart the server  
    def restart_server():  
        response = requests.get(f"{API_URL}/restart_chat_server")  
        return response.json()  

    st.header("Check Server Status")  
    server_url = st.text_input("Enter chat server URL", f"http://{os.getenv('INSOURCE_CHAT_HOST')}")  
    status_button = st.button("Check Status")  

    if status_button:  
        status = check_server_status(server_url)  
        st.write(f"Server status: {status['status']}")  
  
    # Restart server section  
    st.header("Restart Chat Server")  
    restart_button = st.button("Restart Server")  
  
    if restart_button:  
        restart_status = restart_server()  
        st.write(f"Server restart status: {restart_status['status']}")  
  
if add_radio == "Environment Variables":
    # Retrieve the available environment variables from the API  
    response = requests.get(f"{API_URL}/env")  
    env_vars = response.json()  
    
    # Display and edit the environment variables  
    st.header("Environment Variables")  
    updated_env_vars = {}  
    for key, value in env_vars.items():  
        new_value = st.text_input(key, value)  
        updated_env_vars[key] = new_value  
    
    # Add an update button to submit changes  
    if st.button("Update Environment Variables"):  
        response = requests.put(f"{API_URL}/env", json=updated_env_vars)  
        if response.status_code == 200:  
            st.success("Environment variables updated successfully.")  
        else:  
            st.error("Failed to update environment variables.")  

if add_radio == "Tools":
  
    # Create a function to get all tools  
    def get_all_tools():  
        response = requests.get(f"{API_URL}/all_tools")  
        return response.json()  
    
    # Create a function to get toggle tools  
    def get_toggle_tools():  
        response = requests.get(f"{API_URL}/toggle_tools")  
        return response.json()  
    
    # Create a function to disable all tools  
    def disable_all_tools():  
        response = requests.get(f"{API_URL}/disable_all_tools")  
        return response.json()  
    
    # Create a function to toggle a tool  
    def toggle_tool(tool_name):  
        response = requests.post(f"{API_URL}/toggle_tools", json={"name": tool_name})  
        return response.json()  
    
    # Create Streamlit UI  
    st.header("Tools Management")   
    
    tools = get_all_tools()  
    toggle_tools = get_toggle_tools()['tools']
    
    # Create a dictionary to store checkbox states  
    checkbox_states = {}  
    
    # Create checkboxes for each tool  
    for tool in tools:  

        checkbox_states[tool] = st.checkbox(tool, value=tool in toggle_tools, key=tool)  
    
    # Update the toggle_tool function to first disable all tools and then toggle the checked tools  
    def toggle_checked_tools():  
        disable_all_tools()  
    
        for tool, state in checkbox_states.items():  
            if state:  
                toggle_tool(tool)  
    
    toggle_button = st.button("Update Tools")  
    
    if toggle_button:  
        toggle_checked_tools()  
        st.success("Checked tools updated successfully.")  

if add_radio == "Document Upload":
  
    # Create functions for file management  
    def read_all():  
        response = requests.get(f"{API_URL}/readall/")  
        return response.json()  
    
    def upload_file(file, folder, subfolder):  
        files = {"file": file}  
        response = requests.post(f"{API_URL}/upload/{folder}/{subfolder}", files=files)  
        return response.json()  
    
    def delete_file(folder, subfolder, filename):  
        response = requests.delete(f"{API_URL}/delete/{folder}/{subfolder}/{filename}")  
        return response.json()  
    
    # Create Streamlit UI  
    st.header("File Management")  
  
    # Read files section  
    st.subheader("Read Files")  
    read_button = st.button("Read Files")  
  
    if read_button:  
        files = read_all()  
        # Create a DataFrame to display files in a user-friendly table format  
        file_data = []  
        for file in files["files"]:  
            for filename in file["files"]:  
                file_data.append([file["folder"], file["subfolder"], filename])  
    
        file_df = pd.DataFrame(file_data, columns=["Folder", "Subfolder", "Filename"])  
        st.write(file_df)  

    # Upload files section  
    st.subheader("Upload Files")  

    # Folders and subfolders  
    col1, col2 = st.columns(2)  
    with col1:  
        folder_options = ["txts", "pdfs", "words", "csvs", "htmls", "urls", "markdowns", "xmls"]  
        folder = st.selectbox("Select a folder", folder_options)  
    with col2:  
        subfolder = st.text_input("Enter a subfolder")  

    uploaded_file = st.file_uploader("Choose a file")  
  
    if uploaded_file:  
        file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}  
        st.write(file_details)  
        upload_button = st.button("Upload File")  
  
        if upload_button:  
            upload_status = upload_file(uploaded_file, folder, subfolder)  
            if upload_status["filename"]:  
                st.success("File uploaded successfully.") 
  
    # Delete files section  
    st.subheader("Delete Files")  
    delete_expander = st.expander("Delete a file")  
    with delete_expander:  
        col3, col4 = st.columns(2)  
        with col3:  
            folder = st.selectbox("Select a folder", folder_options, key="delete_folder")  
        with col4:  
            subfolder = st.text_input("Enter a subfolder", key="delete_subfolder")  
        filename = st.text_input("Enter the filename to delete")  
  
        if filename:  
            delete_button = st.button("Delete File")  
  
            if delete_button:  
                delete_status = delete_file(folder, subfolder, filename)  
                st.write(delete_status)  
