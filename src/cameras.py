from selenium.webdriver import Chrome

from src.chatgpt import generate_description
from src.extractors.base import BaseExtractor
from src.settings import collection


class Camera:
    def __init__(
        self,
        model: str,
        price: str,
        detailed_link: str,
        category: str,
        brand: str,
        extractor: BaseExtractor,
        images: list = None,
        specs: dict = None,
        description: str = None,
    ) -> None:
        self.model = model
        self.price = price
        self.detailed_link = detailed_link
        self.category = category
        self.brand = brand
        self.extractor = extractor

        self.images = images
        self.specs = specs
        self.description = description

    def _set_images(self, driver: Chrome):
        self.images = self.extractor.get_images(self.detailed_link, driver)

    def _set_specs(self, driver: Chrome):
        self.specs = self.extractor.get_specs(self.detailed_link, driver)

    def _set_description(self):
        self.description = generate_description(
            brand=self.brand, model=self.model, specifications=self.specs
        )

    def build(self, driver: Chrome):
        self._set_images(driver)
        self._set_specs(driver)
        self._set_description()

    def is_in_database(self):
        query = {"$or": [{"brand": self.brand}, {"model": self.model}]}
        existing_camera = collection.find_one(query)
        return existing_camera

    def to_dict(self):
        data = {
            "model": self.model,
            "price": self.price,
            "detailed_link": self.detailed_link,
            "category": self.category,
            "brand": self.brand,
            "images": self.images,
            "specs": self.specs,
            "description": self.description,
        }
        return data


class CameraManager:
    cameras = []

    @classmethod
    def execute_extractor(cls, extractor: BaseExtractor, driver):
        camera_previews = extractor.get_preview(driver)
        for camera_preview in camera_previews:
            camera = Camera(**camera_preview, extractor=extractor)
            if not camera.is_in_database():
                camera.build(driver)
                cls.cameras.append(camera.to_dict())

    @classmethod
    def save_cameras(cls):
        if cls.cameras:
            collection.insert_many(cls.cameras)
            cls.cameras = []  # release cameras after saving them in database
