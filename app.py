import streamlit as st
import pandas as pd
from groq import Groq

# تنظیمات صفحه
st.set_page_config(page_title="AS3600 Durability AI Assistant", page_icon="🛡️")

# گرفتن کلید از سکرت‌ها و ساخت کلاینت Groq
# مطمئن شوید در تنظیمات Streamlit کلید GROQ_API_KEY را وارد کرده‌اید
api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

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
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful structural engineering assistant specializing in AS3600 concrete durability requirements."}
    ]

# نمایش پیام‌های قبلی (به جز پیام سیستم)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# دریافت ورودی کاربر با ظاهر چت
if prompt := st.chat_input("Ask your question here..."):
    # نمایش پیام کاربر
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # پردازش و دریافت جواب از هوش مصنوعی Groq (مدل Llama 3)
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile", # شما می‌توانید از llama3-70b-8192 هم استفاده کنید
                temperature=0.5,
            )
            
            text_response = chat_completion.choices[0].message.content
            st.markdown(text_response)
            
            # ذخیره جواب در تاریخچه
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"⚠️ Error communicating with Groq: {e}")
