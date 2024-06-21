from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get response from Generative AI model
def getGeminiResponse(prompt):
    model = genai.GenerativeModel('gemini-pro')
    query = model.generate_content([prompt])
    # Remove backticks and the "sql" keyword from the response text
    sql_query = query.text.strip().replace('`', '').replace('sql', '')
    return sql_query


# Streamlit app configuration
st.set_page_config(page_title="Text to SQL Translator", page_icon=":robot_face:")
st.header("Text to SQL Translator")

# Input field for user prompt
prompt = st.text_input("Describe your textual SQL query: ", key="input")

# Button to submit the prompt
submit = st.button("Get the SQL Query")

# If submit is clicked
if submit and prompt:
    # Get the SQL query response from Generative AI model
    query = getGeminiResponse(prompt)
    st.subheader("Generated SQL Query")
    st.code(query, language='sql')
