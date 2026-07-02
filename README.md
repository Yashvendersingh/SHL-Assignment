# SHL Assessment Advisor

The SHL Assessment Advisor is a complete solution containing a web scraper, a conversational AI agent backend (built with FastAPI), and a client interface. It helps hiring professionals find the right SHL assessments from the catalog based on their specific hiring needs.

## Features
- **Web Scraper**: Extracts product catalog data from SHL's product catalog website and saves it to a structured JSON file.
- **FastAPI Backend API**: A conversational endpoint that powers the agent, including semantic search capabilities using `sentence-transformers` and fallback mechanisms.
- **Generative AI Integration**: Powered by Google Gemini (gemini-2.0-flash) for intelligent dialogue and requirements gathering.
- **HTML Client**: A simple web UI to interact with the API right out of the box.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Recommended: Create a virtual environment

### 2. Install Dependencies
Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```
To run tests, you may also want to install `pytest` and `httpx`:
```bash
pip install pytest httpx
```

### 3. Generate Catalog Data (Optional)
The project comes with a pre-built `shl_catalog.json` file. If you want to fetch fresh data from the SHL catalog, run the scraper script:

```bash
python scraper.py
```

### 4. Configuration (Optional)
By default, the agent will use local semantic search and keyword fallback to make recommendations. To enable natural conversational abilities, set your Gemini API key:
- **Windows (PowerShell)**: `$env:GEMINI_API_KEY="your_api_key_here"`
- **Linux/Mac**: `export GEMINI_API_KEY="your_api_key_here"`

## Running the Application

### Start the Server
Start the FastAPI server on port 8000 using uvicorn:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Open the Client UI
Once the server is running, simply double-click the `client.html` file in the project folder to open it in your web browser. You can immediately start chatting with the agent!

## Testing

To run the automated test suite for the API and agent logic, run:

```bash
pytest
```
