import streamlit as st
import pandas as pd
from groq import Groq

# تنظیمات صفحه
st.set_page_config(page_title="AS3600 Durability AI Assistant", page_icon="🛡️")

# گرفتن کلید از سکرت‌ها و ساخت کلاینت Groq
if "GROQ_API_KEY" not in st.secrets:
    st.error("کلید GROQ_API_KEY در فایل secrets تنظیم نشده است!")
    st.stop()

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

# تابع برای تبدیل دیتافریم به متن جهت ارسال به مدل
@st.cache_data
def get_csv_text():
    df = load_data()
    if df is not None:
        return df.to_csv(index=False)
    return ""

# بازگرداندن بخش View Database
with st.expander("View Database"):
    df = load_data()
    if df is not None:
        st.dataframe(df)
    else:
        st.error("⚠️ Error: 'data.csv' file not found!")

# آماده‌سازی دیتابیس متنی
csv_data_text = get_csv_text()

# تعریف System Prompt بسیار سخت‌گیرانه
SYSTEM_PROMPT = f"""
You are an expert structural engineering assistant specializing in AS3600. 
Below is the strictly provided database containing durability requirements.

--- START OF DATABASE ---
{csv_data_text}
--- END OF DATABASE ---

STRICT INSTRUCTIONS:
1. You MUST answer the user's questions USING ONLY the information in the database above.
2. If the answer cannot be found directly in the provided database, you MUST refuse to answer and reply EXACTLY with:
"I don't know. My information is strictly limited to the provided database."
3. DO NOT use any of your pre-existing knowledge. DO NOT guess. DO NOT provide data from outside this CSV text.
4. If you output any math formulas or variables, ALWAYS use $...$ or $$...$$ delimiters.
"""

# مقداردهی اولیه برای تاریخچه چت
if "messages" not in st.session_state:
    st.session_state.messages = []
    # پیام سیستم (پنهان از کاربر) را به عنوان اولین پیام اضافه می‌کنیم
    st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})

# نمایش پیام‌های قبلی (به جز پیام سیستم)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# دریافت ورودی کاربر با ظاهر چت
if prompt := st.chat_input("Ask your question here..."):
    # نمایش پیام کاربر
    with st.chat_message("user"):
        st.markdown(prompt)
        
    st.session_state.messages.append({"role": "user", "content": prompt})

    # پردازش و دریافت جواب از هوش مصنوعی Groq
    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.0, # مهم: تنظیم روی صفر برای جلوگیری از تولید اطلاعات خارج از فایل
            )
            
            text_response = chat_completion.choices[0].message.content
            st.markdown(text_response)
            
            # ذخیره جواب در تاریخچه
            st.session_state.messages.append({"role": "assistant", "content": text_response})
            
        except Exception as e:
            st.error(f"⚠️ Error communicating with Groq: {e}")
