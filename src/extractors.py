from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium_utils import (
    click_picture,
    scroll_page_to_bottom,
    specs_see_more,
    wait_for_page_load,
)


class BaseExtractor(ABC):
    BASE_URL: str
    CATEGORIES: list

    @abstractmethod
    def get_preview(self, driver: Chrome) -> List[dict]:
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


class SonyExtractor(BaseExtractor):
    BASE_URL = "https://electronics.sony.com"
    CATEGORIES = ["all-interchangeable-lens-cameras"]

    @classmethod
    def get_preview(cls, driver: Chrome) -> list:
        camera_previews = []
        for category in cls.CATEGORIES:
            url = f"{cls.BASE_URL}/imaging/interchangeable-lens-cameras/c/{category}"
            print(url)
            driver.get(url)
            wait_for_page_load(driver)
            scroll_page_to_bottom(driver)
            wait_for_page_load(driver)

            page_source = driver.page_source
            soup = get_soup(page_source)
            camera_elements = soup.find_all(
                "li", {"class": "col-12 col-sm-6 col-md-6 col-lg-4"}
            )

            div_category = soup.find("div", class_="custom-product-list")
            for camera in camera_elements:
                price_div = camera.find("div", class_="custom-product-grid-item__price")
                camera_dict = {
                    "brand": "Sony",
                    "model": camera.find("p").text.strip()
                    if camera.find("p")
                    else camera.find(
                        "a", class_="custom-product-grid-item__info"
                    ).text.strip(),
                    "price": price_div.text.strip() if price_div else "Not Available",
                    "category": div_category.find(
                        "span", class_="custom-sort-element__prod-list__bold__non-search"
                    ).text.strip(),
                    "detailed_link": cls.BASE_URL
                    + camera.find("a", class_="custom-product-grid-item__info")["href"],
                }
                camera_previews.append(camera_dict)

        return camera_previews

    @staticmethod
    def get_specs(url: str, driver: Chrome) -> dict:
        driver.get(url)
        wait_for_page_load(driver)
        specs_see_more(driver)
        soup = get_soup(driver.page_source)
        full_specs = soup.find_all(
            "div", class_="full-specifications__specifications-single-card"
        )

        result = {}
        for full_spec in full_specs:
            keys = full_spec.find_all(
                "h4",
                class_="full-specifications__specifications-single-card__sub-list__name",
            )
            values = full_spec.find_all(
                "p",
                class_="full-specifications__specifications-single-card__sub-list__value",
            )
            if len(keys) == len(values):
                for i in range(len(keys)):
                    result[keys[i].text.strip()] = values[i].text.strip()
        return result

    @staticmethod
    def get_images(url: str, driver: Chrome) -> list:
        driver.get(url)
        wait_for_page_load(driver)
        click_picture(driver, "is-initialized")
        soup = get_soup(driver.page_source)
        picture_divs = soup.find_all("div", class_="carousel-slide")
        image_urls = []
        for div in picture_divs:
            if div.find("app-pdp-carousel-media-element"):
                img = div.find("img", alt=True)
                if img and img.has_attr("src"):
                    image_urls.append(img["src"])
        return image_urls
