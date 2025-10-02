# 🤖 AI Q&A Bot

A versatile AI-powered question-answering application with both command-line and web interfaces.

## Features

- **Dual Interface**: CLI and Streamlit web app
- **Conversation Memory**: Maintains context across questions
- **Export Capabilities**: Save conversations as JSON
- **Statistics Tracking**: Monitor usage metrics
- **Customizable Settings**: Adjust temperature and model parameters

## Quick Start

1. Navigate to project directory: `cd 01-ai-qa-bot`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment: `cp .env.example .env` and add your OpenAI API key
4. Run CLI version: `python cli_version.py`
5. Run Web version: `streamlit run app.py`


## Project Structure

01-ai-qa-bot/
├── app.py # Streamlit web application
├── cli_version.py # Command-line interface
├── ai_engine.py # AI engine and API handlers
├── config.py # Configuration settings
├── requirements.txt # Python dependencies
├── .env.example # Environment template
└── README.md # This file



## Technologies Used

- Python 3.9+
- OpenAI GPT API
- Streamlit for web interface
- python-dotenv for configuration