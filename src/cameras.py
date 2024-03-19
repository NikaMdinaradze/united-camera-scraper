from extractors import BaseExtractor
from selenium.webdriver import Chrome

class Camera:
    def __init__(self,
                 model: str,
                 price: str,
                 detailed_link: str,
                 category: str,
                 brand: str,
                 extractor: BaseExtractor,
                 images: list = None,
                 specs: dict = None,
                 description: str = None) -> None:
        self.model = model
        self.price = price
        self.detailed_link = detailed_link
        self.category = category
        self.brand = brand
        self.extractor = extractor

        self.images = images
        self.specs = specs
        self.description = description

    def set_images(self, driver: Chrome):
        self.images = self.extractor.get_images(self.detailed_link, driver)

    def set_specs(self, driver: Chrome):
        self.specs = self.extractor.get_specs(self.detailed_link, driver)

    def set_description(self, driver: Chrome):
        ...

class CameraManager:
    cameras = []

    @classmethod
    def execute_extractor(cls, extractor: BaseExtractor, driver):
        camera_previews = extractor.get_preview(driver)
        for camera_preview in camera_previews:
            camera = Camera(**camera_preview, extractor=extractor)
            camera.set_images(driver)
            camera.set_specs(driver)
            cls.cameras.append(camera)

    @classmethod
    def save_cameras(cls):
        print(cls.cameras)
