from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_clickable_element_by_xpath(driver, xpath, wait_time):
    return WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_and_click_element_by_xpath(driver, xpath, wait_time):

    clickable_element = get_clickable_element_by_xpath(
        driver, xpath, wait_time)
    clickable_element.click()


def wait_and_send_keys_by_xpath(driver, xpath, input_string, wait_time):
    input_available_element = get_clickable_element_by_xpath(
        driver, xpath, wait_time)
    input_available_element.send_keys(input_string)
