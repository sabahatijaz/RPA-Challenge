from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import os

class SeleniumManager:

    def __init__(self):
        pass

    def get_beautiful_soup(self, driver):
        """returns a bs4 object for a specific chrome page.

        Args:
            driver (selenium.webdriver): instance to selenium webdriver

        Returns:
            BeautifulSoup: bs4 instance
        """
        
        return BeautifulSoup(driver.execute_script('return document.documentElement.outerHTML'), 'html.parser')

    def get_chrome_driver(self):
        """Installs chromedriver if doesnot exists and sets headers for chromedriver.

        Returns:
            selenium.webdriver: webdriver element.
        """
        
        dr = ChromeDriverManager().install()
        
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
        
        prefs = {
            "download.default_directory": path,
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        }
        
        options = Options()
        options.add_experimental_option("prefs", prefs)
        
        driver = webdriver.Chrome(executable_path=dr, options=options)
        
        return driver

    def click_button(self, element, driver):
        """Click on a selenium element using JS.
        """
        
        driver.execute_script("arguments[0].click();", element)
    
    def wait_for_element(self, xpath, driver, t):
        """Wait for an element to load for a specific period.

        Args:
            xpath (str): xpath for html element.
            driver (selenium.Webdriver): chrome webdriver instance
            t (int): time to wait
        """
        
        WebDriverWait(driver, t).until(EC.presence_of_element_located((By.XPATH, xpath)))
