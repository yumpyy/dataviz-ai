Dataviz AI
==========

Dependencies
------------

- langchain
- langchain-community
- langchain_google_genai
- django
- manim

Setup & Run
-----------

1. Create `.env` file with your Gemini API key
```
GOOGLE_API_KEY=your-api-key-here
```

2. Run the following command
```
python -m venv .venv
source .venv/bin/activate
pip install requirements.txt
python manage.py runserver
```
