import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_page_load(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)


def scroll_page(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


def scroll_page_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def click_specifications(driver, ID):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, ID))).click()


def click_view_more(driver, Xpath):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, Xpath))).click()


def click_picture(driver, selector):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, selector))
    ).click()


def specs_see_more(driver):
    click_specifications(driver, "PDPSpecificationsLink")
    click_view_more(driver, "(//button[contains(text(),'See More')])[2]")


def find_load_more(driver, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def scroll_to_load_more(driver, xpath):
    while True:
        try:
            load_more_button = find_load_more(driver, xpath)
            if load_more_button:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
                    load_more_button,
                )
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                time.sleep(1)
                load_more_button.click()
                time.sleep(3)
            else:
                break
        except NoSuchElementException:
            break
        except Exception:
            scroll_page_to_bottom(driver)
            break
