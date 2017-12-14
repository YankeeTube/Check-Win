from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
import time
import requests
from bs4 import BeautifulSoup

class auto_Cams:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        binary = "chromedriver.exe"
        self.driver = webdriver.Chrome(binary, chrome_options=chrome_options)

    def __del__(self):
        if self.driver is None:
            self.driver.quit()

    def wait_element(self, identifier, click=False, all=False):
        # sleep(self.delay)
        if all:
            try:
                elements = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_all_elements_located(identifier)
                )
            except:
                while True:
                    try:
                        elements = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_all_elements_located(identifier)
                        )

                        break
                    except:
                        pass
            return elements
        else:
            try:
                element = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(identifier)
                )
                if click:
                    element.click()
            except:
                while True:
                    try:
                        element = WebDriverWait(self.driver, 15).until(
                            EC.presence_of_element_located(identifier)
                        )
                        if click:
                            element.click()
                        break
                    except:
                        pass

            return element

    # def cams_login(self):
    #     self.driver.get("http://cmms.icams.co.kr") # 주식회사 캠스
    #     id = self.wait_element((By.ID,"PRTUSRID")) # ID
    #     pw = self.wait_element((By.ID,"PRTPWD")) # password
    #
    #     id.send_keys("103403")
    #     pw.send_keys("alsrjs@1")
    #     pw.submit()

    # def link_parser(self):
    #     # html_page = requests.get("http://cmms.icams.co.kr")
    #     html_page = requests.get(self.driver.current_url).content
    #     soup = BeautifulSoup(html_page)
    #     if soup.findAll('a'):
    #         for link in soup.findAll('a'):
    #             print(link.get('href'))
    #     if soup.findAll('link'):
    #         for link in soup.findAll('link'):
    #             print(link.get('href'))

    def test(self):
        self.driver.get("https://support.microsoft.com/ko-kr/help/4009469")
        self.driver.find_element_by_id("side-nav-link-23").click()

if __name__ == '__main__':
    ac = auto_Cams()
    ac.test()