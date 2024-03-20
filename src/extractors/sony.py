from base import BaseExtractor, get_soup
from selenium.webdriver import Chrome

from ..utils import (
    click_picture,
    scroll_page_to_bottom,
    specs_see_more,
    wait_for_page_load,
)


class SonyExtractor(BaseExtractor):
    BASE_URL = "https://electronics.sony.com"
    CATEGORIES = ["all-interchangeable-lens-cameras"]

    @classmethod
    def get_preview(cls, driver: Chrome) -> list:
        camera_previews = []
        for category in cls.CATEGORIES:
            url = f"{cls.BASE_URL}/imaging/interchangeable-lens-cameras/c/{category}"
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
