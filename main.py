from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium_helpers

outlook_email = "virtru-challenge@outlook.com"
outlook_password = "!nsecur3Pa$$word"

driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://outlook.live.com/owa/')

encrypted_email_subject = ''
chosen_email = ''
email_content = 'Sed dignissim netus arcu id egestas ultricies lacus etiam libero mattis augue sit risus, neque magna 🍺🍒💍🏰🎻🐄🐩🕘🍥📊🏯📋💟🎦 mauris facilisis vestibulum eleifend 🔁🐅🎮🐘 nec 🕧🔯👪👸🍕🏆 sit lacus pulvinar quisque morbi maecenas 🌏👠🌐🎲 🍃👡📙💫👅💣 🔚🔞🐊🌗🐾📍🏤🎈💙 mattis suspendisse eu euismod 🍨🎻🍓🕘🏡📤👈🎊🍤📦. Sit ante maecenas pellentesque nibh dignissim amet eget sit sed nulla 🍢🔋🎾🎻🍆🌁🐹🎵🐗🔭 feugiat orci ipsum viverra sit orci condimentum ultricies leo diam orci et orci, nec quam blandit. 🍁🔴🏰🎤💵🌖📔🍤🍈👅👾📕👉🌑 🎿🌶🍒🍸🏧🔤🍸🌒👌🔎💓🍩📌💗 vestibulum vitae dui pellentesque lobortis et sit id pellentesque diam at 🌼👒🗽🎉🔞💒💃👋🌳📡🍋🕜🐭🌻 ipsum convallis dapibus urna faucibus integer cras 🐏🔨🐲🌗🕣👐💠 aenean sed molestie semper a aliquet magna interdum et luctus quis commodo, felis est porttitor commodo.'


outlook_sign_in_xpath = "//*[@class='linkButtonFixedHeader office-signIn']"
email_input_xpath = "//input[@type='email']"
email_submit_button_xpath = "//input[@type='submit'][@value='Next']"
password_submit_button_xpath = "//input[@type='submit'][@value='Sign in']"
email_password_inputxpath = "//input[@type='password']"
virtru_link_regex = '^(https?:\/\/)?(secure)\.(virtru)\.(com)\//?'

ms_doughboy_xpath = "//*[@class='o365cs-mfp-header']//div[@class='o365cs-mfp-doughboy-container']"
unlock_message_link_xpath = "//a[starts-with(@href, 'https://secure.virtru.com/start/?')][text()[contains(.,'Unlock Message')]]"
verify_me_link_xpath = "//a[starts-with(@href, 'https://accounts.virtru.com/email-activation?linkId=')][text()[contains(.,'VERIFY ME')]]"

secure_your_email_title = "//*[@class='login-message']/span[text()[contains(.,'Select your email')]]"
send_me_a_verification_email_xpath = "//a[@class='btn btn-lg auth-choice-btn sendEmailButton']"


def sign_in(email, password):
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, outlook_sign_in_xpath, 2)

    selenium_helpers.wait_and_send_keys_by_xpath(
        driver, email_input_xpath, email, 2)

    selenium_helpers.wait_and_click_element_by_xpath(
        driver, email_submit_button_xpath, 1)

    selenium_helpers.wait_and_send_keys_by_xpath(
        driver, email_password_inputxpath, password, 2)

    selenium_helpers.wait_and_click_element_by_xpath(
        driver, password_submit_button_xpath, 2)


def open_email_with_subject(subject):
    email_with_subject_xpath = "//div[@aria-label='Mail list']//span[@class='lvHighlightAllClass lvHighlightSubjectClass'][text()[contains(.,'" + \
        subject + "')]]"
    # driver.implicitly_wait(5)
    selenium_helpers.get_clickable_element_by_xpath(
        driver, ms_doughboy_xpath, 15)
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, email_with_subject_xpath, 15)

    selenium_helpers.wait_and_click_element_by_xpath(
        driver, unlock_message_link_xpath, 15)
    active_windows = driver.window_handles
    driver.switch_to.window(active_windows[1])


def click_virtru_unlock_message_link(email):

    verify_email_xpath = "//span[@class='userEmail'][text()[contains(.,'" + email + "')]]"
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, verify_email_xpath, 12)

    selenium_helpers.wait_and_click_element_by_xpath(
        driver, send_me_a_verification_email_xpath, 10)

    driver.switch_to.window(driver.window_handles[0])
    # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')


def verify_virtru(email):
    driver.refresh()
    selenium_helpers.get_clickable_element_by_xpath(
        driver, ms_doughboy_xpath, 15)
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, "//*[@role='menu']//span[@title='Other']", 5)
    driver.implicitly_wait(3)
    # this will locate the latest email from verify@virtru.com
    virtru_verification_email_xpath = "//*[@class='lvHighlightAllClass lvHighlightFromClass'][text()[contains(.,'verify@virtru.com')]]"
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, virtru_verification_email_xpath, 5)
    selenium_helpers.wait_and_click_element_by_xpath(
        driver, verify_me_link_xpath, 5)
    driver.switch_to.window(driver.window_handles[1])


def assert_email_contents(expected_email_contents):

    selenium_helpers.get_clickable_element_by_xpath(
        driver, "//div[@id='click-into-reply-view']", 5)

    # get text from email body
    encryped_email_body = selenium_helpers.get_clickable_element_by_xpath(driver,"//*[@id='tdf-body']",5)
    actual_email_contents = encryped_email_body.text
    print(actual_email_contents)
    # assert email text equal to expected_email_contents

    assert expected_email_contents == actual_email_contents


sign_in(outlook_email, outlook_password)
open_email_with_subject("automated-emoji-test")
click_virtru_unlock_message_link(outlook_email)
verify_virtru(outlook_email)
assert_email_contents(email_content)
