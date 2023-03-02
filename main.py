from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import time
import json

class DownloadBot:
    def __init__(self, config):
        self.url = config['url']
        self.service = Service(config['chrome_driver_path'])
        self.options = webdriver.ChromeOptions()
        
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def find_all_items(self):
        self.driver.get(self.url)
        
        self.main_tab = self.driver.current_window_handle
        pages = self.driver.find_element(By.XPATH,"//*[@id='divListItems2']/div/nav/div[2]/ul[2]/li[1]/span[3]")
        pages_int = int(pages.text)

        item_body = self.driver.find_element(By.TAG_NAME, "tbody")
        item_tr_list = item_body.find_elements(By.TAG_NAME, "tr")
        
        
        for item_tr in item_tr_list:
            result_img = item_tr.find_element(By.CLASS_NAME, "result-img")
            self.download_fabric(result_img)
            
        main_tab.close()

        for page in range(1, pages_int+1):
            if page == 1: # no need to click page btn
                pass
            else:
                pass
            
    def download_fabric(self, result_img):
        result_img.click()
        time.sleep(5)
        for window_handle in self.driver.window_handles:
            if window_handle != self.main_tab:
                self.driver.switch_to.window(window_handle)
                body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                print('loaded!!', body)
                break
        time.sleep(3)
        
        # do all the download operations
        
        # close the item tab, and switch to main tab
        self.driver.close()
        self.driver.switch_to.window(self.main_tab)
            

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    bot = DownloadBot(config)
    bot.find_all_items()

    while True:
        pass