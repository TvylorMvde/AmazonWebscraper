from selenium import webdriver

DIRECTORY = "reports"
NAME = "Playstation 4"
CURRENCY = "€"
MIN_PRICE = "300"
MAX_PRICE = "400"
FILTERS = {
    "min": MIN_PRICE,
    "max": MAX_PRICE
}
URL = "https://www.amazon.de/"

def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)

def get_web_driver_options():
    return webdriver.ChromeOptions()

def set_ignore_certificate_error(options):
    options.add_argument("--ignore-certificate-errors")

def set_browser_as_incognito(options):
    options.add_argument("--incognito")

# Initialize Chome browser in a headless mode 
# def set_automation_as_head_less(options):
#     options.add_argument("--headless")


