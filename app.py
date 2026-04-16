import streamlit as st
import pandas as pd
import google.generativeai as genai

# تنظیمات صفحه
st.set_page_config(page_title="AS3600 Durability AI Assistant", page_icon="🛡️")

# --- تنظیم کلید API به صورت مستقیم ---
api_key = "AQ.Ab8RN6K5tlhID9PX3L3S0VeOz74eO6_Qm9coMixMfVEbNZQiNw"
genai.configure(api_key=api_key)
# -----------------------------------

# عنوان و توضیحات
st.title("🛡️ AS3600 Durability AI Assistant")
st.write("Ask me anything about concrete durability requirements (AS3600 - Section 4)!")

# بارگذاری فایل CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
        return df
    except Exception as e:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Error: 'data.csv' file not found! Please make sure it is uploaded to GitHub.")
else:
    # نمایش پیش‌نمایش دیتا (اختیاری)
    with st.expander("View Database"):
        st.dataframe(df)

    # کادر دریافت سوال از کاربر
    user_question = st.chat_input("Ask your question here...")

    if user_question:
        # نمایش سوال کاربر
        with st.chat_message("user"):
            st.write(user_question)

        # ارسال به هوش مصنوعی و نمایش جواب
        with st.chat_message("assistant"):
            with st.spinner("Analyzing data..."):
                try:
                    # تبدیل اطلاعات فایل اکسل/CSV به متن برای هوش مصنوعی
                    data_context = df.to_string(index=False)
                    
                    # ساخت پرامپت (دستور) برای جمنای
                    prompt = f"""
                    You are an expert structural engineer assisting with AS3600 (Concrete Structures Standard - Durability Section).
                    Based ONLY on the following data table, please answer the user's question accurately.
                    
                    Data Table:
                    {data_context}
                    
                    User Question: {user_question}
                    """
                    
                    # فراخوانی مدل
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    
                    # نمایش جواب
                    st.write(response.text)
                
                except Exception as e:
                    st.error(f"❌ API Error: {e}")
                    st.warning("لطفاً بررسی کنید که آیا API Key شما برای Google Gemini معتبر است یا خیر.")
