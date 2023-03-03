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
        self.item_list = []
        
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.wait = WebDriverWait(self.driver, 30)
    
    def find_all_items(self):
        self.driver.get(self.url)
        
        self.main_tab = self.driver.current_window_handle
        pages = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='divListItems2']/div/nav/div[2]/ul[2]/li[1]/span[3]")))
        pages_int = int(pages.text)

        for page in range(pages_int):
            try:
                item_body = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
                next_page_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='divListItems2']/div/nav/div[2]/ul[1]/li[8]/div")))
                item_tr_list = item_body.find_elements(By.TAG_NAME, "tr")
            except StaleElementReferenceException:
                print('StaleElementReferenceException error')
            
            for item_tr in item_tr_list:
                result_img = item_tr.find_element(By.CLASS_NAME, "result-img")
                self.download_fabric(result_img)
            
            time.sleep(5)
            next_page_btn.click()
            time.sleep(3)
            
        return self.item_list
            
    def download_fabric(self, result_img):
        result_img.click()
        
        for window_handle in self.driver.window_handles:
            if window_handle != self.main_tab:
                self.driver.switch_to.window(window_handle)
                item_rows = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr")))
                print('loaded!!')
                break
        time.sleep(1)
        
        # do all the download operations
        row_size = len(item_rows)
        name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='main3']/div[1]/div/div[1]/div[1]/b"))).text
        id = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[1]/td[3]").text.split(' ')[0]
        
        if row_size == 4:
            size = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[3]/td[2]").text
            era = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[4]/td[2]").text
            desc = ''
            
        elif row_size == 5:
            condition = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[2]/td[1]").text
            
            if condition == '分類':
                size = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[3]/td[2]").text
                era = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[4]/td[2]").text
                desc = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[5]/td[2]").text
                
            elif condition == '品名':   
                size = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[4]/td[2]").text
                era = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[5]/td[2]").text
                desc = ''
                
            else:
                print("something I didn't recognize yet") 
            
        elif row_size == 6: 
            size = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[4]/td[2]").text
            era = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[5]/td[2]").text
            desc = self.driver.find_element(By.XPATH, "//*[@id='collapseExample']/div/div[1]/table/tbody/tr[6]/td[2]").text
            
        time.sleep(1)
        ITEM = {
            "id": id,
            "name": name,                
            "size": size,
            "era": era,
            "desc": desc
        }
        self.item_list.append(ITEM)
            
        # close the item tab, and switch to main tab
        self.driver.close()
        self.driver.switch_to.window(self.main_tab)

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json.load(config_file)
    
    bot = DownloadBot(config)
    items = bot.find_all_items()
