# Proxy Scraper and Rotator

This project contains two Python scripts that demonstrate how to scrape and rotate **free proxies** using requests, BeautifulSoup, and Scrapy.

## proxies.py

This script defines a class called Proxy that fetches and tests proxies from different sources. It has four methods:

- `__init__`: Initializes the class with some URLs for proxy sources, custom headers, and empty lists for proxies.
- `get_proxies`: Fetches proxies from the specified URLs and filters them based on some criteria.
- `test_proxy`: Tests a proxy by making a request using it and returns True or False depending on the response status code and any exceptions.
- `save_good_proxies`: Tests and saves the good proxies to a list.

The proxy sources used in this script are:

- [hidemy.io]: This website offers free proxies that are updated every 10 minutes and have various features such as anonymity, speed, and country.
- [free-proxy-list.net]: This website offers free proxies that are updated every 15 minutes and have various features such as anonymity, speed, and country.

## proxy_rotation.py

This script defines a class called UpworkSpider that inherits from scrapy.Spider and scrapes data from a website using proxies. It has five methods:

- `__init__`: Initializes the class with some custom settings for the spider, such as the feed format, the concurrent requests, and the download delay.
- `start_requests`: Sends the initial request with a randomly chosen proxy from the list of good proxies obtained from the Proxy class.
- `parse`: Parses the response and extracts the desired data.
- `retry_callback`: Handles any errors or failures in the request and retries it with a different proxy until it succeeds.
- `get_headers`: Returns a random user agent for each request.

## How to run

To run the scripts, you need to have Python 3 and the following libraries installed:

- requests
- BeautifulSoup
- Scrapy

You can install them using `pip install...`.

Then, you can run the proxy_rotation.py script using `python proxy_rotation.py`. This will scrape the data from the website using the good proxies and save it to a JSON file. You don't need to run the proxies.py script. It will be imported as a library into the proxy_rotation.py file
