import scrapy
import random
from scrapy.crawler import CrawlerProcess
from proxies import Proxy # Import the Proxy class from the proxies module
from scrapy.spidermiddlewares.httperror import HttpError



class UpworkSpider(scrapy.Spider):
    name = 'upworkscraper'
    # Create an instance of the Proxies class
    proxies = Proxy()
    # Set custom settings for the spider
    custom_settings = {
        "FEEDS": {
            "result.json": {"format": "json"}
        },
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DOWNLOAD_DELAY": 2,
    }

    current_page = 1
    # Update the start_requests() method to use a good proxy
    def start_requests(self):

        url = "https://httpbin.org/get"
        headers = self.get_headers()
        proxy = "http://"+random.choice(self.proxies.good_proxies)

        print("\nCURRENT START PROXY", proxy)
        # Send the initial request with the chosen proxy
        yield scrapy.Request(url=url,
                             headers=headers,
                             meta={'proxy': proxy, "url" : url, "download_timeout": 20},
                             callback=self.parse,
                             errback=self.retry_callback,
                             )

    def parse(self, response):
        pass

    def retry_callback(self, failure):
        if failure.check(HttpError):
            response = failure.value.response
            status_code = response.status
            self.logger.error(f"\nHttpError {status_code} on {response.url}: RETRYING...")
        else:
            request = failure.request
            print(f"\nERROR: RETRYING...")
            print(request.url)
        self.logger.error(repr(failure))
        url = failure.request.meta["url"]
        headers = self.get_headers()

        # Now explicitly set the proxy for the retry
        proxy = "http://" + random.choice(self.proxies.good_proxies)
        print("\nCURRENT RETRY PROXY", proxy)

        # Retry the request with the new proxy
        yield scrapy.Request(url=url,
                             headers=headers,
                             meta={'proxy': proxy, "url": url},
                             callback=self.parse,
                             errback=self.retry_callback,
                             dont_filter=True)



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
            "User-Agent": random.choice(user_agents), # Choose a random user agent
        }

        return headers
    
if __name__ == "__main__":
    # Configure settings for the CrawlerProcess
    process = CrawlerProcess()
    process.crawl(UpworkSpider)
    process.start()



