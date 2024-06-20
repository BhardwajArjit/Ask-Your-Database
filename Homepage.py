import streamlit as st


def main():
    st.set_page_config(
        page_title="Project M",
        page_icon="👋",
    )

    st.title("Generative AI Project")
    st.markdown("##### Welcome to our Generative AI Project! This project comprises two powerful components designed to simplify database querying and SQL generation through natural language interaction.")
    st.markdown("## Overview")
    st.markdown("Our project aims to revolutionize the way you interact with your MySQL databases by leveraging the power of AI. It includes two main components:")
    st.markdown("1. **Ask Your Database**: An interactive chat application that allows you to query your MySQL database using natural language. This component translates your questions into SQL queries, executes them, and returns the results in an easy-to-understand format.")
    st.markdown("2. **Text to SQL Translator**: A tool that accepts English prompts and returns the corresponding SQL queries. This component is ideal for users who need to generate SQL queries without writing them manually.")
    st.sidebar.success("Select a page above.")


if __name__ == '__main__':
    main()
