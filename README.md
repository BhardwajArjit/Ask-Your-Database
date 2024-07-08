# Ask Your Database: Interactive Database Querying and Text to SQL Translator

Welcome to Ask Your Database! This project comprises two powerful components designed to simplify database querying and SQL generation through natural language interaction.

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Contribution](#contribution)
7. [License](#license)

## Overview

Our project aims to revolutionize the way you interact with your MySQL or PostgreSQL databases by leveraging the power of AI. It includes two main components:

1. **Chat with Database**: An interactive chat application that allows you to query your localhost MySQL or PostgreSQL database using natural language. This component translates your questions into SQL queries, executes them, and returns the results in an easy-to-understand format.
   
2. **Text to SQL Translator**: A tool that accepts English prompts and returns the corresponding SQL queries. This component is ideal for users who need to generate SQL queries without writing them manually.

## Features

- **Natural Language Processing**: Convert plain English questions into SQL queries.
- **Interactive Chat Interface**: Easy-to-use chat interface for querying databases.
- **Real-time Query Execution**: Execute queries on your MySQL or PostgreSQL database and get instant results.
- **SQL Generation**: Generate SQL queries from English prompts.

## Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

- Python 3.x
- MySQL Server
- PostgreSQL Server
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BhardwajArjit/Ask-Your-Database.git
    cd Ask-Your-Database
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables. Create a `.env` file in the root directory and add your Google API key:
    ```plaintext
    GOOGLE_API_KEY=your_google_api_key
    ```

4. Run the application:
    ```bash
    streamlit run Homepage.py
    ```

## Usage

1. **Launch the Application**: Open your browser and navigate to the Streamlit app (usually `http://localhost:8501`).
2. **Connect to Your Database**: Use the sidebar to enter your MySQL or PostgreSQL database connection details and click "Connect".
3. **Ask Questions**: Type your questions in the chat input at the bottom of the page.

## Code Structure

- `Homepage.py`: The main application file.
- `requirements.txt`: Lists the required Python packages.
- `.env`: Environment variables for sensitive information like API keys.

## Contribution

If you'd like to contribute to the project, feel free to fork the repository and submit a pull request. We welcome all contributions that improve the functionality and user experience of the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

This application uses the following technologies:

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://www.openai.com/)
- [Google Generative AI](https://cloud.google.com/ai-generative)
