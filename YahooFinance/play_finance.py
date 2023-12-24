# Importing necessary modules and classes
import random
import requests
import asyncio
from bs4 import BeautifulSoup
import json
from playwright.async_api import async_playwright
from urllib.parse import urlencode

# Defining a spider class for web scraping
class FinanceSpider():
    def __init__(self):
        # Base URLs for different finance categories
        self.base_urls = [
            "https://finance.yahoo.com/most-active?",
            "https://finance.yahoo.com/gainers?",
            "https://finance.yahoo.com/losers?"
            ]
        # List to store extracted links
        self.links = []
        # Initializing the spider
        self.entry_point()

    # Method to start the requests
    def entry_point(self):
        # Getting headers for the requests
        headers = self.get_headers()
        # Generating requests for the initial page
        for url in self.base_urls:
            params = {
                "offset":"0",
                "count":"100"
            }
            url = url + urlencode(params)
            try:
                # Sending GET request
                response = requests.get(url=url, headers=headers)
                print("GET REQUEST:", response)
                # Parsing the response
                self.parse(response)
            except Exception as e:
                print("\nEXCEPTION:",e)

        # Generating requests for the next page
        for url in self.base_urls:
            params = {
                "offset":"100",
                "count":"100"
            }
            next_page = url + urlencode(params)
            try:
                # Sending GET request for the next page
                response = requests.get(url=next_page, headers=headers)
                print("GET REQUEST:", response)
                self.parse(response)
            except Exception as e:
                print("\nEXCEPTION:", e)
           
    # Method to parse the response
    def parse(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        # Extracting data from the response
        table = soup.find("table", class_='W(100%)').find("tbody").find_all("tr")
        
        for data in table:
            symbol = data.find("a", {"data-test" : "quoteLink"}).get_text()
            link = f"https://finance.yahoo.com/quote/{symbol}/history?p={symbol}" 
            name = data.find("td", {"aria-label" : "Name"}).get_text()
            
            stock = {"symbol" : symbol,
                     "link" : link,
                     "name" : name}
            self.links.append(stock)
        print(self.links)

                  
    # Method to extract financial data from HTML response
    def get_data(self, response, symbol, name):
        try:
            soup = BeautifulSoup(response, "lxml")
            rows = soup.find("table", class_="W(100%) M(0)").find("tbody").find_all("tr")
            print(len(rows))
            for row in rows:
                try:
                    # Extracting individual data points from each row  
                    data = row.find_all("td")
                    date = data[0].find("span").get_text()
                    _open = data[1].find("span").get_text()
                    high = data[2].find("span").get_text()
                    low = data[3].find("span").get_text()
                    close = data[4].find("span").get_text()
                    adj_close = data[5].find("span").get_text()
                    volume = data[6].find("span").get_text()
                except Exception as e:
                    print("\nEXCEPION:", e)
                    break
                else:
                    # Extracting individual data points from each row
                    stock_data = {
                        "symbol" : symbol,
                        "name" : name,
                        "date" : date,
                        "open" : _open,
                        "high" : high,
                        "low" : low,
                        "close" : close,
                        "adj_close" : adj_close,
                        "volume" : volume
                    }

                    print(stock_data)
                    # Printing the extracted data
                    print(stock_data)
                    # Writing the data to a JSON file
                    with open("financeresult.json", "a") as json_file:
                        json.dump(stock_data, json_file)
                        json_file.write(",\n")

        except Exception as e:
            print("\nEXCEPION:", e)


    # Method to fetch HTML content of a URL using Playwright
    async def extract_data(self, url, symbol, name):
        print("\nOPENING BROWSER...")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless = False)
            page = await browser.new_page()
            headers = self.get_headers()
            # Configuring the browser page
            await page.set_viewport_size(
                {"width": 1200, "height": 1880}
            )
            await page.set_extra_http_headers(headers)
            # Navigating to the URL and waiting for the page to load
            await page.goto(url, timeout=120000)
            await page.wait_for_load_state("domcontentloaded")
            # Simulating scrolling to load additional content
            for _ in range(1,8):
                await page.keyboard.press("End")
                await asyncio.sleep(2)
            # Extracting the page content
            page_content = await page.content()
            # Extracting data from the HTML content
            self.get_data(page_content, symbol, name)
            await browser.close()


    async def main(self, concurrency_limit=3):
        semaphore = asyncio.Semaphore(concurrency_limit)

        async def limited_extract_data(url):
            async with semaphore:
                await self.extract_data(url["link"], url["symbol"], url["name"])

        tasks = [limited_extract_data(url) for url in self.links]
        await asyncio.gather(*tasks)


    # Method to generate random user-agent headers
    def get_headers(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 OPR/95.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.0 Safari/537.36"
        ]
        headers={
            "User-Agent": random.choice(user_agents),
        }

        return headers    

# Entry point for the script
if __name__ == "__main__":
    # Configure settings for the CrawlerProcess
    spider = FinanceSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.main())
    
