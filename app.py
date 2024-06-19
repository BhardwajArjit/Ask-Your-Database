from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
from urllib.parse import quote_plus


def initPostgresDatabase(user: str, password: str, host: str, port: str, database: str):
    """
    Initialize the connection to the PostgreSQL database.

    Args:
        user (str): The database user.
        password (str): The database user's password.
        host (str): The database host.
        port (str): The database port.
        database (str): The name of the database.

    Returns:
        SQLDatabase: The SQLDatabase object representing the connection.
    """
    encoded_password = quote_plus(password)
    db_uri = f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def initMysqlDatabase(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    """
    Initialize the connection to the MySQL database.

    Args:
        user (str): The database user.
        password (str): The database user's password.
        host (str): The database host.
        port (str): The database port.
        database (str): The name of the database.

    Returns:
        SQLDatabase: The SQLDatabase object representing the connection.
    """
    encoded_password = quote_plus(password)
    db_uri = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


def getSqlChain(db):
    """
    Create a chain of operations to generate an SQL query from a user's natural language question.

    Args:
        db (SQLDatabase): The SQLDatabase object representing the connection.

    Returns:
        RunnablePassthrough: A chain of operations that generate the SQL query.
    """
    template = """You are a data analyst at a company. You are interacting with a user who is asking you questions 
    about the company's database. Based on the table schema below, write a SQL query that would answer the user's 
    question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;

    Your turn:

    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 google_api_key=os.getenv("GOOGLE_API_KEY"),
                                 temperature=0.7, top_p=0.85)

    def getSchema(_):
        """
        Retrieve the schema information from the database.

        Args:
            _ : Placeholder for the argument.

        Returns:
            str: The schema information.
        """
        return db.get_table_info()

    return (
            RunnablePassthrough.assign(schema=getSchema)
            | prompt
            | llm
            | StrOutputParser()
    )


def getResponse(userQuery: str, db: SQLDatabase, chatHistory: list):
    """
    Generate a natural language response to the user's question based on the database content.

    Args:
        userQuery (str): The user's natural language question.
        db (SQLDatabase): The SQLDatabase object representing the connection.
        chatHistory (list): The history of the chat interaction.

    Returns:
        str: The natural language response to the user's question.
    """
    sql_chain = getSqlChain(db)

    template = """You are a data analyst at a company. You are interacting with a user who is asking you questions 
    about the company's database. Based on the table schema below, question, sql query, and sql response, 
    write a natural language response. <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                                 google_api_key=os.getenv("GOOGLE_API_KEY"),
                                 temperature=0.7, top_p=0.85)

    chain = (
            RunnablePassthrough.assign(query=sql_chain).assign(
                schema=lambda _: db.get_table_info(),
                response=lambda variables: db.run(variables["query"]),
            )
            | prompt
            | llm
            | StrOutputParser()
    )

    return chain.invoke({
        "question": userQuery,
        "chat_history": chatHistory,
    })


if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
    ]

load_dotenv()

st.set_page_config(page_title="Ask Your Database", page_icon=":robot_face:")

st.title("Ask Your Database")

with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")

    st.text_input("Host", value="localhost", key="Host")
    st.text_input("Port", value="3306", key="Port")
    st.text_input("User", value="root", key="User")
    st.text_input("Password", type="password", value="", key="Password")
    st.text_input("Database", value="", key="Database")

    if st.button("Connect"):
        with st.spinner("Connecting to database..."):
            db = initMysqlDatabase(
                st.session_state["User"],
                st.session_state["Password"],
                st.session_state["Host"],
                st.session_state["Port"],
                st.session_state["Database"]
            )
            st.session_state.db = db
            st.success("Connected to database!")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = getResponse(user_query, st.session_state.db, st.session_state.chat_history)
        st.markdown(response)

    st.session_state.chat_history.append(AIMessage(content=response))
