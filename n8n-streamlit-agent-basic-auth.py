import streamlit as st
import requests
import uuid
import re

# Hàm đọc nội dung từ file văn bản
def rfile(name_file):
    try:
        with open(name_file, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
            st.error(f"File {name_file} không tồn tại.")

# Constants
BEARER_TOKEN = st.secrets.get("BEARER_TOKEN")
WEBHOOK_URL = st.secrets.get("WEBHOOK_URL")

def generate_session_id():
    return str(uuid.uuid4())

def send_message_to_llm(session_id, message):
    headers = {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "sessionId": session_id,
        "chatInput": message
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        print("Request payload:", payload)
        response.raise_for_status()
        response_data = response.json()
        print("Full response:", response_data)
        
        contract = response_data[0].get('contract', "No contract received")
        url = response_data[0].get('url', "No URL received")
        
        return [{"json": {"contract": contract, "url": url}}]
    
    except requests.exceptions.RequestException as e:
        return [{"json": {"contract": f"Error: Failed to connect to the LLM - {str(e)}", "url": ""}}]

def display_output(output):
    """Hiển thị nội dung hợp đồng và URL file Word"""
    contract = output.get('json', {}).get('contract', "No contract received")
    urlWord = output.get('json', {}).get('url',"No file recceived")
    print("urlWorld: ",urlWord)
    st.markdown(contract, unsafe_allow_html=True)
    
    if urlWord and urlWord != "No URL received":
        st.markdown(
            f"""
            <a href="{urlWord}" target="_blank" style="color: blue; text-decoration: underline;">
                Xem file hợp đồng (Word)
            </a>
            """,
            unsafe_allow_html=True
        )

def main():
    st.set_page_config(page_title="Trợ lý AI", page_icon="🤖", layout="centered")

    # Thêm mã CSS để tùy chỉnh footer
    st.markdown("""
        <style>
            footer {
                visibility: hidden;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            .assistant {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none; /* Màu trong suốt */
                text-align: left;
            }
            .user {
                padding: 10px;
                border-radius: 10px;
                max-width: 75%;
                background: none; /* Màu trong suốt */
                text-align: right;
                margin-left: auto;
            }
            .assistant::before { content: "🤖 "; font-weight: bold; }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    try:
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            st.image("logo.png")
    except:
        pass
    
    try:
        with open("00.xinchao.txt", "r", encoding="utf-8") as file:
            title_content = file.read()
    except Exception as e:
        title_content = "Trợ lý AI"

    st.markdown(
        f"""<h1 style="text-align: center; font-size: 24px;">{title_content}</h1>""",
        unsafe_allow_html=True
    )
