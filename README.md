# SQL Agent

SQL Agent is a tool designed to interact with SQLite databases using natural language queries. It leverages LangChain and LangGraph to provide a seamless interface for executing SQL commands, managing workflows, and handling errors effectively.

## Features

- Execute SQL queries against a SQLite database.
- Automatically check and correct SQL queries for common mistakes.
- Retrieve database schema and list tables.
- Handle errors gracefully with fallback mechanisms.
- Structured workflow management using LangGraph.

## Directory Structure

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/Sql_Agent.git
    cd Sql_Agent
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Environment Variables:**

    The application requires an OpenAI API key. You can set it by running:

    ```bash
    export OPENAI_API_KEY=your_api_key_here
    ```

    Alternatively, the application will prompt you to enter it if not set.

## Usage

1. **Run the application:**

    ```bash
    python main.py
    ```

2. **Running Tests:**

    ```bash
    python -m unittest discover tests
    ```

## Configuration

All configuration settings are located in the `config/settings.py` file. You can modify environment variables and other settings as needed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.