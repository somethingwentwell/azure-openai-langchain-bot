# write a streamlit app that takes customer name as input,                  
# after submit the input, show "Generating Powerpoint",                  
# then wait for 5 seconds to show a download button,                  
# clicking the download button to download ./BEA_Test_1.pptx from server   

import streamlit as st  
import time  
from io import BytesIO  
from PIL import Image  
import os  

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
  
def main():  
    st.title("InSource AI PowerPoint Generator")  
      
    customer_name = st.text_input("Enter customer name:")  
      
    if st.button("Submit"):  
        st.write("Searching for Customer Information...")  
        time.sleep(2)  
        st.write("Generating PowerPoint...")  
        time.sleep(5)  
          
        if os.path.exists("./BEA_Test_1.pptx"):  
            with open("./BEA_Test_1.pptx", "rb") as f:  
                ppt_data = f.read()  
              
            ppt_bytes = BytesIO(ppt_data)  
            st.write("PowerPoint generated! Click the button below to download.")  
            st.download_button(  
                label="Download PowerPoint",  
                data=ppt_bytes,  
                file_name="BEA_Test_1.pptx",  
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",  
            )  
        else:  
            st.write("Error: PowerPoint file not found on the server.")  
  
if __name__ == "__main__":  
    main()  
