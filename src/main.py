from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from cameras import CameraManager
from extractors import NikonExtractor

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

nikon_extractor = NikonExtractor()
cameras = nikon_extractor.get_preview(driver)
CameraManager.execute_extractor(nikon_extractor, driver)
CameraManager.save_cameras()

driver.quit()
