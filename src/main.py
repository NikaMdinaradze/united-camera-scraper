from cameras import CameraManager
from extractors.canon import CanonExtractor
from extractors.nikon import NikonExtractor
from extractors.sony import SonyExtractor
from settings import get_driver

def main():
    driver = get_driver()

    nikon_extractor = NikonExtractor()
    CameraManager.execute_extractor(nikon_extractor, driver)

    sony_extractor = SonyExtractor()
    CameraManager.execute_extractor(sony_extractor, driver)

    canon_extractor = CanonExtractor()
    CameraManager.execute_extractor(canon_extractor, driver)

    CameraManager.save_cameras()

    driver.quit()

if __name__ == "__main__":
    main()
