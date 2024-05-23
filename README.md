# Ask Your Database

Welcome to "Ask Your Database", a simple and interactive chat application designed to make querying your MySQL database easier through natural language interaction. This application uses the power of AI to translate your questions into SQL queries, execute them on your database, and provide you with easy-to-understand responses.

## Features

- **Natural Language Interaction**: Simply ask questions about your database in plain English.
- **Automated SQL Query Generation**: The application automatically converts your questions into SQL queries.
- **Seamless Database Connection**: Connect to your MySQL database with ease.
- **Conversation History**: Keeps track of your interaction history for a more personalized experience.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/BhardwajArjit/Text-to-SQL-Translator.git
    cd Text-to-SQL-Translator
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
    streamlit run app.py
    ```

## Usage

1. **Launch the Application**: Open your browser and navigate to the Streamlit app (usually `http://localhost:8501`).
2. **Connect to Your Database**: Use the sidebar to enter your MySQL database connection details and click "Connect".
3. **Ask Questions**: Type your questions in the chat input at the bottom of the page.

## Example

1. **Connecting to the Database**:
    - Host: `localhost`
    - Port: `3306`
    - User: `root`
    - Password: `your_password`
    - Database: `your_database_name`

2. **Asking Questions**:
    - "List the first 10 entries."
    - "Who has got the highest marks?"

The AI will convert these questions into SQL queries, execute them, and provide the results in a human-readable format.

## Code Structure

- `app.py`: The main application file.
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
