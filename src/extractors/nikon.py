from typing import List

from base import BaseExtractor, get_soup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from ..utils import wait_for_page_load


class NikonExtractor(BaseExtractor):
    BASE_URL = "https://www.nikonusa.com"
    CATEGORIES = ["compact-digital-cameras", "dslr-cameras", "mirrorless-cameras"]

    @classmethod
    def get_preview(cls, driver: Chrome) -> list:
        camera_previews = []
        for category in cls.CATEGORIES:
            url = f"{cls.BASE_URL}/en/nikon-products/{category}/index.page"
            driver.get(url)
            wait_for_page_load(driver)
            select_element = driver.find_element(By.ID, "nkn-resp-items-per-page")
            select = Select(select_element)
            select.select_by_value("-1")
            page_source = driver.page_source
            soup = get_soup(page_source)
            cameras = soup.find_all("li", class_="nkn-resp-filter-entry")

            for camera in cameras:
                url = (
                    cls.BASE_URL + camera.find("a", class_="product-detail-link")["href"]
                )
                camera_dict = {
                    "brand": "Nikon",
                    "model": camera.find("span", itemprop="name").text.strip(),
                    "price": camera.find("span", itemprop="price").text.strip(),
                    "detailed_link": url,
                    "category": category,
                }
                camera_previews.append(camera_dict)
        return camera_previews

    @staticmethod
    def get_images(url: str, driver: Chrome) -> List[str]:
        driver.get(url)
        wait_for_page_load(driver)
        page_source = driver.page_source
        soup = get_soup(page_source)
        image_container = soup.find("ol", class_="carousel-inner")
        images = image_container.find_all("img")
        image_urls = []

        for image in images:
            if "data-pend-src" in image.attrs:
                image_urls.append(image["data-pend-src"])
            else:
                image_urls.append(image["src"])
        return image_urls

    @staticmethod
    def get_specs(url: str, driver: Chrome) -> dict:
        driver.get(url + "#tab-ProductDetail-ProductTabs-TechSpecs")
        wait_for_page_load(driver)
        page_source = driver.page_source
        soup = get_soup(page_source)
        specs = soup.find_all("li", class_=["spec-content", "row"])
        result = {}
        for spec in specs:
            key = spec.find("h4", class_=["spec-title", "col-sm-6"])
            value = spec.find("div", class_=["specs col-sm-6"])
            result[key.get_text(strip=True)] = value.get_text(strip=True)
        return result
