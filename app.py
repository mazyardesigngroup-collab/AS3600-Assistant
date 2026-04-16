import streamlit as st
import pandas as pd
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AS3600 AI Assistant", layout="centered")

st.title("🛡️ AS3600 Durability AI Assistant")
st.write("Ask me anything about concrete durability requirements (AS3600 - Section 4)!")
st.divider()

# Load API Key from Streamlit Secrets
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("Error: GOOGLE_API_KEY not found in Streamlit Secrets!")
    st.stop()

# Load CSV Data
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

try:
    df = load_data()
    
    # User Input Section
    user_question = st.text_input("Enter your question (e.g., 'What is the exposure classification for a coastal area?'):")

    if st.button("Ask AI 🧠"):
        if not user_question:
            st.warning("⚠️ Please enter a question first.")
        else:
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Create Prompt with Context
            context = df.to_string()
            prompt = f"""
            You are an expert structural engineering assistant specializing in the Australian standard AS3600.
            Using the table data provided below, give a precise and accurate answer to the user's question.
            If the answer cannot be found in the provided table, clearly state that you don't have enough information based on the current data.
            Provide your answer in professional, clear engineering English.

            Table Data:
            {context}

            User Question: {user_question}
            """

            # Show a loading spinner while waiting for the response
            with st.spinner("Analyzing AS3600 standard... ⏳"):
                response = model.generate_content(prompt)
                st.success("Response:")
                st.info(response.text)

except FileNotFoundError:
    st.error("Error: 'data.csv' not found! Make sure it is located in the same directory as app.py.")
except Exception as e:
    st.error(f"System Error: {e}")
