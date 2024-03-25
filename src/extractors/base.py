from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome

from src.extractors.schemas import CameraPreview


class BaseExtractor(ABC):
    BASE_URL: str
    CATEGORIES: list

    @abstractmethod
    def get_preview(self, driver: Chrome) -> List[CameraPreview]:
        pass

    @staticmethod
    @abstractmethod
    def get_images(url: str, driver: Chrome) -> List[str]:
        pass

    @staticmethod
    @abstractmethod
    def get_specs(url: str, driver: Chrome) -> dict:
        pass


def get_soup(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    return soup
