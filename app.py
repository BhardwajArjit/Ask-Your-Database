from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import re

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Function to get response from Generative AI model
def getGeminiResponse(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text.strip()


# Function to execute SQL query
def readSQLQuery(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# Prompt for generic SQL query handling
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION. 

    Examples of supported queries:

    1. How many entries of records are present?
       Example SQL: SELECT COUNT(*) FROM STUDENT;

    2. Tell me all the students studying in Data Science class?
       Example SQL: SELECT * FROM STUDENT WHERE CLASS="Data Science";

    3. Give all the students' names.
       Example SQL: SELECT NAME FROM STUDENT;

    4. Show me the students in the Computer Science class with the name starting with 'A'.
       Example SQL: SELECT * FROM STUDENT WHERE CLASS="Computer Science" AND NAME LIKE 'A%';

    5. What is the section of the student named 'John'?
       Example SQL: SELECT SECTION FROM STUDENT WHERE NAME="John";

    Please note that the SQL code should not have ``` in the beginning or end, and SQL word in the output.
    """
]


# Streamlit app configuration
st.set_page_config(page_title="Text to SQL Translator")
st.header("App To Retrieve SQL Data")

# Input field for user question
question = st.text_input("Input: ", key="input")

# Button to submit the question
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    # Get the SQL query response from Generative AI model
    response = getGeminiResponse(question, prompt)
    st.subheader("Generated SQL Query")
    st.code(response)

    # Execute the SQL query
    query_result = readSQLQuery(response, "student.db")

    # Display the response
    st.subheader("The Response is")
    if query_result:
        # Convert the query result to string and use regex to extract numbers and words
        result_str = ' '.join(map(str, query_result))
        clean_result = re.sub(r'[^\w\s]', '', result_str)  # Remove brackets and commas
        st.write(clean_result)
    else:
        st.write("No results found")
