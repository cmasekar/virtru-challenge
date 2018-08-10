from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_clickable_element_by_xpath(driver, xpath, wait_time):
    """ Limiting locator type to XPATHs"""
    try:
        return WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException:
        print("Selenium TimeoutException when trying to find element with xpath: " + str(xpath))
        print("Closing browser!")
        driver.close()


def click_element_by_xpath(driver, xpath, wait_time):

    clickable_element = find_clickable_element_by_xpath(
        driver, xpath, wait_time)
    clickable_element.click()


def send_keys_to_element_by_xpath(driver, xpath, input_string, wait_time):
    input_available_element = find_clickable_element_by_xpath(
        driver, xpath, wait_time)
    input_available_element.send_keys(input_string)
