import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
import time


def browser_options_setup():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()

    headers = {"Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1","Referrer":"https://www.google.com/"}

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--mute-audio")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-web-security")
    options.add_argument("--incognito")
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--lang=en-GB")
    # options.add_argument("--headless")

    options.set_capability("acceptInsecureCerts", True)
    return options, user_agent, headers

def spawn_browser(options, user_agent, headers):
    browser = webdriver.Chrome('C:\\Users\mandah-acer\Downloads\EXE\chromedriver.exe', options=options)
    browser.header = headers
    browser.header['User-Agent'] = user_agent
    return browser

start = time.time()
url = 'https://amazon.com'
options, user_agent, headers = browser_options_setup()
browser = spawn_browser(options, user_agent, headers)
browser.get(url)
browser.implicitly_wait(5)
