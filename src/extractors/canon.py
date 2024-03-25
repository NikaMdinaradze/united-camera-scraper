from selenium.webdriver import Chrome

from src.extractors.base import BaseExtractor, get_soup
from src.extractors.schemas import CameraPreview
from src.utils import scroll_to_load_more, wait_for_page_load


class CanonExtractor(BaseExtractor):
    BASE_URL = "https://www.usa.canon.com/"
    CATEGORIES = ["mirrorless-cameras", "dslr-cameras", "compact-cameras"]

    @classmethod
    def get_preview(cls, driver: Chrome) -> list:
        camera_previews = []
        for category in cls.CATEGORIES:
            url = f"https://www.usa.canon.com/shop/cameras/{category}"
            driver.get(url)
            wait_for_page_load(driver)
            scroll_to_load_more(
                driver,
                "//button[@class='primary amscroll-load-button' and @amscroll_type='after']",
            )
            page_source = driver.page_source
            soup = get_soup(page_source)
            amscroll_divs = {}
            for i in range(1, 4):
                amscroll_divs[f"page_{i}"] = soup.find_all(
                    "div", attrs={"amscroll-page": str(i)}
                )
            for page, divs in amscroll_divs.items():
                for div in divs:
                    div_html = str(div)
                    div_soup = get_soup(div_html)

                    camera_names = div_soup.find_all(
                        "h2", class_="product name product-item-name"
                    )
                    price_spans = div_soup.find_all("span", class_="normal-price")
                    for name, price_span in zip(camera_names, price_spans):
                        camera_dict = {
                            "brand": "Canon",
                            "model": name.get_text(strip=True),
                            "price": price_span.find("span", class_="price").get_text(
                                strip=True
                            ),
                            "detailed_link": f"{name.find('a', class_='product-item-link').get('href')}?color=Black&type=New",
                            "category": category,
                        }
                        validated_data = CameraPreview.validate_dict(camera_dict)
                        camera_previews.append(validated_data)

        return camera_previews

    @staticmethod
    def get_images(url: str, driver: Chrome) -> list:
        driver.get(url)
        wait_for_page_load(driver)
        page_source = driver.page_source
        soup = get_soup(page_source)
        photos = soup.find_all(
            "div", class_="fotorama__thumb fotorama__loaded fotorama__loaded--img"
        )
        image_urls = []
        for photo in photos:
            image_urls.append(photo.find("img", class_="fotorama__img")["src"])
        return image_urls

    @staticmethod
    def get_specs(url: str, driver: Chrome):
        driver.get(url)
        wait_for_page_load(driver)
        page_source = driver.page_source
        soup = get_soup(page_source)

        spec_classes = " ".join(["tech-spec", "xml", "cms-accordion", "attr-group-info"])
        pdf_classes = " ".join(["tech-spec", "pdf", "cms-accordion", "attr-group-info"])

        spec_divs = soup.find_all("div", class_=lambda x: x and spec_classes in x)
        pdf_div = soup.find("div", class_=lambda y: y and pdf_classes in y)
        specs_data = {}
        for specs in spec_divs:
            keys = specs.find_all("div", class_="tech-spec-attr attribute")
            values = specs.find_all("div", class_="tech-spec-attr attribute-value")
            for key, value in zip(keys, values):
                key_text = key.get_text(strip=True)
                value_text = value.get_text(strip=True)
                specs_data[key_text] = value_text

            specs_data["pdf"] = (
                pdf_div.find("a")["href"] if pdf_div and pdf_div.find("a") else None
            )
        return specs_data
