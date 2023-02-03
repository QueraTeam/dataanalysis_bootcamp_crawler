from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# selenium servise


from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
# Chrome servise

from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as firefoxeService
# Firefox servise

from webdriver_manager.microsoft  import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
# Edge servise


class CrawlerTool(object):
    
    def __init__(self, browser:str) -> None:
        self._check_witch_browser(browser)
        self._url = r'https://www.alibaba.ir'
            
    def _check_witch_browser(self, browser):
        match browser:
            case 'firefox':
                service = firefoxeService(executable_path=GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service)
                
           
            case _:
                raise ValueError('your chosen browser is not found! valid options:(chrome, firefox, edge)')

    def _make_url(self):
        raise Exception()

    def _open_page(self):
        raise Exception()

        




    
    

