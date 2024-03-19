from abc import ABC, abstractmethod
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from selenium_utils import wait_for_page_load

class BaseExtractor(ABC):
    BASE_URL: str
    CATEGORIES: list
    @abstractmethod
    def get_preview(self, driver: Chrome) -> list:
        pass

    @abstractmethod
    def get_images(self, url: str, driver: Chrome) -> dict:
        pass

    @abstractmethod
    def get_specs(self, url: str, driver: Chrome) -> dict:
        pass

