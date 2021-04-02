import urllib.request
from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
import time
import pandas as pd


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
    options.add_argument('log-level=3')
    options.add_argument("--headless")

    options.set_capability("acceptInsecureCerts", True)
    return options, user_agent, headers

def spawn_browser(options, user_agent, headers):
    #change here according to your driver path
    browser = webdriver.Chrome('C:\\Users\mandah-acer\Downloads\EXE\chromedriver.exe', options=options)
    browser.header = headers
    browser.header['User-Agent'] = user_agent
    return browser
    
def save_request_details(result):
    df = pd.DataFrame(result)
    #change here according to file path
    #df.to_excel("C:\\Users\\mandah-acer\\Documents\\webcrawler\\crawling_result.xlsx")
    df.to_csv("C:\\Users\\mandah-acer\\Documents\\webcrawler\\crawling_result.csv")

def get_requests_details(browser, result):
    count = 0
    for request in browser.requests:
        if request.response:
            request_url = request.url
            request_date = request.date
            request_language = request.headers['Accept-Language']
            request_user_agent = request.headers['User-Agent']        
            response_date = request.response.date
            response_status = request.response.status_code
            response_content_type = request.response.headers['Content-Type']
            count += 1
            result.append({"url": browser.current_url, "webpage_title": browser.title, "request_url": request_url, "request_date": request_date, "request_language": request_language, "request_user_agent": request_user_agent, "response_date": response_date, "response_status": response_status, "response_content_type": response_content_type})
            save_request_details(result)
            print(request_url, request_date, request_language, request_user_agent, response_date, response_status, response_content_type)
        if count == 10: break # to limit only to get 10 earliest requests, comment to disable

result = []
start = time.time()
options, user_agent, headers = browser_options_setup()
browser = spawn_browser(options, user_agent, headers)
#change here according to your url list name
url_file = open("url_list.txt", "r")
url_list = url_file.read().replace("\n",",").split(",")
url_list = [url for url in url_list if url != ""]
print("URL List:", url_list)

for url in url_list:
    print("Processing:", url)
    try:
        browser.get(url)
        browser.implicitly_wait(5)
        get_requests_details(browser, result)
    except Exception:
        continue
    print("Current results count:", len(result))
    print("Elapsed Time: {}(s)".format(round(time.time()-start,2)))
