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
        print(links)


    def get_products_links(self):
        self.driver.get(self.url)
        search_bar = self.driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
        search_bar.send_keys(self.search)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(2)
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        print(f"Our url {self.driver.current_url}")
        time.sleep(2)
        result_list = self.driver.find_elements_by_class_name('s-result-list')
        links = []
        try:
            results = result_list[0].find_elements_by_xpath('//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a')
            for link in results:
                links.append(link.get_attribute('href'))
        except Exception as e:
            print("Didn't get any products...")
            print(e)
        return links


if __name__ == "__main__":
    scraper = AmazonAPI(NAME, FILTERS, URL, CURRENCY)
    data = scraper.run()
