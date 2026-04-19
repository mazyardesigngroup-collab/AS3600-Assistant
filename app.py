import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AS3600 Durability AI Assistant", page_icon="🛡️")

# گرفتن کلید از سکرت‌ها
api_key = st.secrets["GOOGLE_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

st.title("🛡️ AS3600 Durability AI Assistant")
st.write("Ask me anything about concrete durability requirements (AS3600 - Section 4)!")

# --- (کدهای مربوط به لود کردن فایل data.csv را اینجا نگه دارید) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Error: 'data.csv' file not found!")
# ------------------------------------------------------------------

user_input = st.text_input("سوال خود را بپرسید:")

if st.button("ارسال"):
    if user_input:
        # ارسال درخواست مستقیم به API گوگل
        payload = {
            "contents": [{"parts": [{"text": user_input}]}]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            st.success(text_response)
        else:
            st.error(f"خطا در ارتباط با سرور: {response.status_code}")
            st.write(response.json())
