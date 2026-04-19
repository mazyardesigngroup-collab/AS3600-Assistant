import streamlit as st
import pandas as pd
import requests

# تنظیمات صفحه
st.set_page_config(page_title="AS3600 Durability AI Assistant", page_icon="🛡️")

# گرفتن کلید از سکرت‌ها و تنظیم URL
api_key = st.secrets["GOOGLE_API_KEY"]
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

st.title("🛡️ AS3600 Durability AI Assistant")
st.write("Ask me anything about concrete durability requirements (AS3600 - Section 4)!")

# تابع لود کردن دیتا
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv") # مطمئن شوید فایل دیتا کنار app.py باشد
        return df
    except Exception as e:
        return None

# بازگرداندن بخش View Database
with st.expander("View Database"):
    df = load_data()
    if df is not None:
        st.dataframe(df)
    else:
        st.error("⚠️ Error: 'data.csv' file not found!")

# مقداردهی اولیه برای تاریخچه چت
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش پیام‌های قبلی
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# دریافت ورودی کاربر با ظاهر چت
if prompt := st.chat_input("Ask your question here..."):
    # نمایش پیام کاربر
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # پردازش و دریافت جواب از هوش مصنوعی
    with st.chat_message("assistant"):
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                text_response = result["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(text_response)
                # ذخیره جواب در تاریخچه
                st.session_state.messages.append({"role": "assistant", "content": text_response})
            else:
                error_msg = f"API Error: {response.status_code}"
                st.error(error_msg)
                st.write(response.json())
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        except Exception as e:
            st.error(f"Connection Error: {e}")
