import streamlit as st  
import asyncio  
from websockets import client
import json
import os
import requests

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

def send_receive_messages_api(rest_uri_uri, message, aiMsg):
    try:
        response = requests.post(rest_uri_uri, json=message)
        response = response.json()
        if response.get("result"):
            aiMsg.write(response['result'])  
        else:
            aiMsg.write(f"**error** Please contact your administrator.")
    except Exception as e:
        aiMsg.write(f"**error** {e}")

async def send_receive_messages_ws(websocket_uri, message, aiMsg):
    async with client.connect(websocket_uri) as websocket:  
        await websocket.send(json.dumps(message))  
        while websocket.open:
            response = await websocket.recv()  
            response = json.loads(response)
            try:
                if response.get("result"):
                    aiMsg.write(f"**result** {response['result']}")  
                elif response.get("callback"):
                    aiMsg.write(f"**{response['callback']}** {response['thought']}")
                else:
                    aiMsg.write(f"**error** Please contact your administrator.")
            except Exception as e:
                aiMsg.write(f"**error** {e}")

async def main():
    st.title("InSource Test")  
    session_id = st.text_input("Session ID:")
    user_input = st.chat_input("Type your message:")  

    with st.sidebar:
        add_radio = st.radio(
            "Select Type",
            ("RESTAPI", "WebSocket")
        )

    if add_radio == "RESTAPI":
        st.subheader("REST API")
        rest_uri = st.text_input("Chat Server Host", f"http://{os.getenv('INSOURCE_CHAT_HOST')}/run")
        if user_input:  
            userMsg = st.chat_message("user")
            aiMsg = st.chat_message("assistant")
            userMsg.write(user_input)  
            req = {
                "id": "rest-st-" + session_id,
                "text": user_input
            }
            send_receive_messages_api(rest_uri, req, aiMsg) 

    if add_radio == "WebSocket":
        st.subheader("Websocket")
        websocket_uri = st.text_input("Chat Server Host", f"ws://{os.getenv('INSOURCE_CHAT_HOST')}/ws")
        if user_input:  
            userMsg = st.chat_message("user")
            aiMsg = st.chat_message("assistant")
            userMsg.write(user_input)  
            req = {
                "id": "ws-st-" + session_id,
                "text": user_input
            }
            await send_receive_messages_ws(websocket_uri, req, aiMsg)  


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
