from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get response from Generative AI model
def getGeminiResponse(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([question])
    return response.text.strip()


# Streamlit app configuration
st.set_page_config(page_title="Text to SQL Translator")
st.header("Text to SQL Translator")

# Input field for user question
question = st.text_input("Describe your textual SQL query: ", key="input")

# Button to submit the question
submit = st.button("Get the SQL Query")

# If submit is clicked
if submit and question:
    # Get the SQL query response from Generative AI model
    response = getGeminiResponse(question)
    st.subheader("Generated SQL Query")
    st.code(response, language='sql')
