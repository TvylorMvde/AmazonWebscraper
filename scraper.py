import time
import json
import re
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
        if not links:
            print("Script stopped.")
            return
        print(f"Got {len(links)} links to products...")
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()
        return products


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


    def get_products_info(self, links):
        asins = self.get_asins(links)
        products = []
        for asin in asins:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products


    def get_single_product_info(self, asin):
        print(f"Product ID: {asin} - getting data...")
        product_short_url = self.shorten_url(asin)
        self.driver.get(f"{product_short_url}?language=en_GB")
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url' : product_short_url,
                'title' : title,
                'seller' : seller,
                'price' : price
            }
            return product_info
        return None


    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get a title of a product - {self.driver.current_url}")
            return None


    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get a seller of a product - {self.driver.current_url}")
            return None


    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id('availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_id('olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(f"Can't find price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
                print(e)
                print(f"Can't find price of a product - {self.driver.current_url}")
                return None
        return price


    def convert_price(self, price):
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + "." + price.split(",")[1]
        except:
            Exception()
        return float(price)


    def shorten_url(self, asin):
        return self.url + 'dp/' + asin


    def get_asins(self, links):
        return [self.get_asin(link) for link in links]


    @staticmethod
    def get_asin(product_link):
        return re.search('/dp/(.+?)/ref', product_link).group(1)



if __name__ == "__main__":
    scraper = AmazonAPI(NAME, FILTERS, URL, CURRENCY)
    data = scraper.run()
    print('smth')
