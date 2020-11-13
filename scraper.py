import time
import json
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from config import (
    get_chrome_web_driver,
    get_web_driver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    DIRECTORY,
    NAME,
    CURRENCY,
    FILTERS,
    URL
)

class GenerateReport:
    def __init__(self):
        pass


class AmazonAPI:
    
    def __init__(self, search, filters, url, currency):
        self.search = search
        self.url = url
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"
        self.currency = currency
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)


    def run(self):
        print("Starting a script...")
        print(f"Looking for {self.search} products...")
        links = self.get_products_links()
        return None


    def get_products_links(self):
        self.driver.get(self.url)
        search_bar = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        search_bar.send_keys(self.search)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)


if __name__ == "__main__":
    scraper = AmazonAPI("Playstation 5", FILTERS, URL, CURRENCY)
    data = scraper.run()