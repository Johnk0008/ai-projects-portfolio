# RBI NBFC Scale Based Regulation Chatbot

A chatbot that answers questions about RBI's Master Directions on NBFC Scale Based Regulation using Google Gemini AI.

## Features
- PDF document processing
- Question-answering using AI
- Evaluation framework
- Simple in-memory document store

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Add Google API key to `.env` file
3. Run setup: `python main.py --setup`
4. Ask questions: `python main.py --question "Your question"`

## Evaluation
Run evaluation: `python main.py --evaluate`