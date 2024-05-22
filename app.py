from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get response from Generative AI model
def getGeminiResponse(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt.format(question=question)])
    return response.text.strip()


# Function to execute SQL query
def readSQLQuery(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
    except sqlite3.Error as e:
        rows = None
        st.error(f"An error occurred: {e}")
    conn.close()
    return rows


# Prompt for generic SQL query handling
prompt = """
You are an expert in converting English questions to SQL queries!
The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION, MARKS.

Convert the following question to a SQL query: "{question}"

The SQL code should not have ``` in the beginning or end, and SQL word in the output.
"""

# Streamlit app configuration
st.set_page_config(page_title="Text to SQL Translator")
st.header("App To Retrieve SQL Data")

# Initialize the recognizer
recognizer = sr.Recognizer()


# Function to capture voice input and convert it to text
def getVoiceInput():
    with sr.Microphone() as source:
        st.write("Listening for your question...")
        audio = recognizer.listen(source)
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand the audio.")
        except sr.RequestError:
            st.write("Sorry, there was an error with the speech recognition service.")
    return ""


# Button to capture voice input
voice_input = st.button("Capture Voice Input")

# Initialize the question variable
question = ""

# If voice input button is clicked, capture the voice input
if voice_input:
    question = getVoiceInput()

# Input field for user question, using the voice input if available
question = st.text_input("Input: ", value=question, key="input")

# Button to submit the question
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    # Get the SQL query response from Generative AI model
    response = getGeminiResponse(question, prompt)

    # Extract the SQL command using regex
    sql_match = re.search(r"SELECT.*?;", response, re.DOTALL | re.IGNORECASE)
    if sql_match:
        sql_query = sql_match.group(0)
        st.subheader("Generated SQL Query")
        st.code(sql_query)

        # Execute the SQL query
        query_result = readSQLQuery(sql_query, "student.db")

        # Display the response
        st.subheader("The Response is")
        if query_result:
            # Convert the query result to a flat string and use regex to remove unwanted characters
            result_str = ' '.join(map(str, query_result))
            clean_result = re.sub(r'[^\w\s]', '', result_str)  # Remove brackets and commas
            st.write(clean_result)
        else:
            st.write("No results found")
    else:
        st.error("Failed to generate a valid SQL query.")