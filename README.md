# ChatGPT Chat History Search

This project, **ChatGPT Chat History Search**, facilitates the search and visualization of chat history using a simple set of instructions. It leverages the power of FastAPI. The goal is to help you efficiently search through your chat history data.

## Getting Started

To get started with using the **ChatGPT Chat History Search** project, follow these steps:

1. **Clone the Repository:** Begin by cloning this repository to your local machine.

2. **Add Conversations Data:** Place your chat history data in the form of a `conversations.json` file within the repository's directory.

3. **Generate Chat History Excel:** Run the `read_chat.py` script using Python. This script processes the `conversations.json` file and generates an Excel file named `chat.xlsx` containing organized chat data.

4. **View Chat History:** Execute the `run.bat` batch file, which will open the generated `chat.xlsx` file in your default web browser. This Excel file is designed to provide a user-friendly interface for searching and viewing your chat history.

## Requirements

Ensure that you have the following requirements met before using the **ChatGPT Chat History Search** project:

- **Python 3.5 or newer:** Make sure you have a compatible Python version installed on your system.

- **FastAPI:** Install the FastAPI library, which is utilized to create the web-based interface for searching chat history.

- **Pandas:** Install the Pandas library, which is used for data processing and manipulation.

- **OpenPyXL:** Install the OpenPyXL library, which enables the generation of Excel files in Python.

You can install these dependencies using the following command:
```bash
pip install fastapi pandas openpyxl
