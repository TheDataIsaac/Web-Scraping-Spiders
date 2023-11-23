import requests
from bs4 import BeautifulSoup
import random

class Proxy:
    def __init__(self):
        # initial URL
        self.hidemy_url = "https://hidemy.io/en/proxy-list/?type=s&anon=234#list"
        self.free_proxy_url = "https://free-proxy-list.net/"
        # custom headers

        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.47",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.0 Safari/537.36"
        ]

        self.proxy_list=[]
        self.good_proxies=[]
        self.get_proxies()
        self.save_good_proxies()

    def get_proxies(self):
        # make initial HTTP request
        url = self.hidemy_url
        response = requests.get(url, headers={"User-Agent": random.choice(self.user_agents)})
        # parse response
        content = BeautifulSoup(response.text, 'lxml')
        table = content.find("table").find("tbody").find_all("tr")

        for proxy in table:
            ip_address=proxy.find_all("td")[0].get_text()
            port=proxy.find_all("td")[1].get_text()
            _proxy=":".join([ip_address,port])
            if url == self.free_proxy_url:
                if (proxy.find_all("td")[4].get_text()) =="elite proxy" and (proxy.find_all("td")[6].get_text()) == "yes":
                    self.proxy_list.append(_proxy)
            else:
                self.proxy_list.append(_proxy)

    # Add a new method to test a proxy using Scrapy
    def test_proxy(self, proxy, url):
        try:
            # Create a Scrapy request with the proxy
            proxy =f"http://{proxy}" 
            print("\nCURRENT TEST PROXY:",proxy)
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
        

    # Implement a new method to test the proxies
    def save_good_proxies(self):
        # Get a list of proxies from the Proxies class
        print(self.proxy_list)

        # Test each proxy
        for proxy in self.proxy_list:
            is_working = self.test_proxy(proxy, "https://httpbin.org/get")
            
            # If the proxy is working, add it to a list of good proxies
            if is_working:
                self.good_proxies.append(proxy)
            
            if len(self.good_proxies) == 5:
                break

        print("\nLIST OF GOOD PROXIES:", self.good_proxies)


if __name__=="__main__":
    proxies = Proxy()