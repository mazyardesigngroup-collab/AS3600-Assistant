import streamlit as st
import pandas as pd

st.set_page_config(page_title="AS3600 - Chapter 4", layout="centered")

# خواندن فایل داده جدید
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
    
    st.title("🛡️ Durability & Cover Requirements")
    st.write("Demo for Chapter 4 - AS3600")
    st.divider()

    # ساخت منوی اول
    environments = df['General Environment'].unique()
    selected_env = st.selectbox("1. Select General Environment:", environments)

    # ساخت منوی دوم بر اساس انتخاب منوی اول
    filtered_df = df[df['General Environment'] == selected_env]
    conditions = filtered_df['Specific Condition'].unique()
    selected_cond = st.selectbox("2. Select Specific Condition:", conditions)

    # پیدا کردن جواب نهایی
    result = filtered_df[filtered_df['Specific Condition'] == selected_cond].iloc[0]

    # نمایش جواب
    st.divider()
    st.subheader("📊 Results")
    
    col1, col2 = st.columns(2)
    col1.metric("Exposure Class", str(result['Exposure Class']))
    col2.metric("Minimum f'c (MPa)", str(result["Min f'c (MPa)"]))

except FileNotFoundError:
    st.error("فایل data.csv پیدا نشد! لطفا مطمئن شوید آن را درست در پوشه Demo_AS3600 ساخته‌اید.")
except Exception as e:
    st.error(f"خطا: {e}")

