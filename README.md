# News Parser for Lenta.ru

A Python web application that fetches news from Lenta.ru and displays them in a browser using Flask.

## Features
- Fetches news with titles, URLs, and publication time.
- Displays news in a clean HTML template.
- Handles errors gracefully (returns "No news" if fetching fails).

## Tech Stack
- Python 3.8+
- Flask (web framework)
- aiohttp (async HTTP requests)
- BeautifulSoup (HTML parsing)

## Installation
1. Clone the repository:
   git clone https://github.com/Kreesk/lenta-news-aggregator.git
   cd lenta-news-aggregator

2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the application:
   python main.py

5. Open http://127.0.0.1:3000/news in your browser.
