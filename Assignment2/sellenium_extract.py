import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementNotVisibleException
)


def get_all_download_links(driver, url):
    '''Visits a page and retrieves all download links using regex'''
    driver.get(url)
    try:
        while True:
            button = driver.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "loadmore")))
            button.click()
    except ElementNotVisibleException:
        pass
    matches = re.findall(
        r'(?<=href=\")/download/.+.jpg(?=\")', driver.page_source)
    return matches