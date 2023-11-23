import requests
from bs4 import BeautifulSoup
import random

class Proxy:
    def __init__(self):
        # Define URLs for proxy sources
        self.urls = ["https://free-proxy-list.net/", "https://hidemy.io/en/proxy-list/?type=s&anon=234#list"]
        
        # Define custom headers for HTTP requests
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.0 Safari/537.36"
        ]

        # Initialize lists to store proxy information
        self.proxy_list=[]
        self.good_proxies=[]
        # Call methods to fetch and test proxies
        self.get_proxies()
        self.save_good_proxies()

    # Method to fetch proxies from specified URLs
    def get_proxies(self):
        for url in self.urls:
            # Make an initial HTTP request to fetch proxies
            response = requests.get(url, headers={"User-Agent": random.choice(self.user_agents)})
            # Parse the response using BeautifulSoup
            content = BeautifulSoup(response.text, 'lxml')
            table = content.find("table").find("tbody").find_all("tr")
            # Extract proxy information from the table
            for proxy in table:
                ip_address=proxy.find_all("td")[0].get_text()
                port=proxy.find_all("td")[1].get_text()
                _proxy=":".join([ip_address,port])
                # Filter proxies based on specific criteria for free-proxy-list.net
                if url == self.urls[0]:
                    if (proxy.find_all("td")[4].get_text()) =="elite proxy" and (proxy.find_all("td")[6].get_text()) == "yes":
                        self.proxy_list.append(_proxy)
                else:
                    self.proxy_list.append(_proxy)

    # Method to test a proxy by making a request using it
    def test_proxy(self, proxy, url):
        try:
            # Create a Scrapy request with the proxy
            proxy =f"http://{proxy}" 
            print("\nCURRENT TEST PROXY:",proxy)
            # Make a request using the proxy
            response = requests.get(url, proxies={"http" : proxy}, headers={"User-Agent": random.choice(self.user_agents)})
            # Check if the response status code is 200
            if response.status_code == 200:
                print("\nRESPONSE", response.status_code)
                return True
            else:
                print("\nRESPONSE", response.status_code)
                return False
        except Exception as e:
            print("\nEXCEPTION", e)
            return False
        

    # Method to test and save good proxies
    def save_good_proxies(self):
        # Print the list of all proxies
        print(self.proxy_list)

        # Test each proxy
        for proxy in self.proxy_list:
            is_working = self.test_proxy(proxy, "https://httpbin.org/get")
            
            # If the proxy is working, add it to a list of good proxies
            if is_working:
                self.good_proxies.append(proxy)
                
            # Break after testing 15 proxies    
            if len(self.good_proxies) == 16:
                break

        # Print the list of good proxies
        print("\nLIST OF GOOD PROXIES:", self.good_proxies)


if __name__=="__main__":
    proxies = Proxy() # Create an instance of the Proxy class