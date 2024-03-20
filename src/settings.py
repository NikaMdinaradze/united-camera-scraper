import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient

# database configuration
MONGO_USERNAME = os.getenv("DATABASE_USERNAME")
MONGO_PASSWORD = os.getenv("DATABASE_PASSWORD")
MONGO_HOST = os.getenv("DATABASE_HOST")
MONGO_PORT = os.getenv("DATABASE_PORT")

uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
client = MongoClient(uri)
db = client["development"]
collection = db["cameras"]

# chatgpt configuration
API_KEY = os.getenv("API_KEY")

# driver configuration
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--incognito")

    # Generating random user-agents
    ua = UserAgent()
    user_agent = ua.random

    chrome_options.add_argument(f"--user-agent={user_agent}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    return driver