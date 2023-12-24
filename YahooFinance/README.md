# Yahoo Finance Scraper

This Python script scrapes financial data from Yahoo Finance and extracts historical stock data for the most active, gaining, and losing stocks. It demonstrates asynchronous web scraping techniques using `asyncio` and `Playwright` for efficient and dynamic content retrieval.

## Key Features:

- **Asynchronous Execution:** Leverages `asyncio` and `Playwright` for concurrent requests and DOM manipulation, enhancing performance and handling dynamic content effectively.
- **Financial Data Extraction:** Extracts comprehensive stock data, including symbol, name, date, open, high, low, close, adjusted close, and volume.
- **Data Storage:** Saves extracted data in a structured JSON format for analysis and further processing.

## How It Works:

1. **Target URLs:** Fetches initial stock lists from three Yahoo Finance pages: most active, gainers, and losers.
2. **Link Extraction:** Parses responses using BeautifulSoup to extract individual stock links.
3. **Asynchronous Data Collection:** Iterates through links, initiating asynchronous tasks for each:
    - Launches a headless browser (Playwright) to handle dynamic content.
    - Navigates to individual stock pages.
    - Simulates scrolling to load additional data.
    - Extracts financial data using BeautifulSoup.
4. **Data Storage:** Saves extracted data in a JSON file named `financeresult.json`.


