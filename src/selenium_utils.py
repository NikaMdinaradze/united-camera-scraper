from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def wait_for_page_load(driver):
    WebDriverWait(driver,
                  10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

def scroll_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
