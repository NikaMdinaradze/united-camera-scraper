from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cameras import CameraManager
from extractors import NikonExtractor, SonyExtractor

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

nikon_extractor = NikonExtractor()
CameraManager.execute_extractor(nikon_extractor, driver)

sony_extractor = SonyExtractor()
CameraManager.execute_extractor(sony_extractor, driver)

CameraManager.save_cameras()

driver.quit()
