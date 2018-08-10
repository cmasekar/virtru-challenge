from selenium import webdriver
import selenium_helpers

OUTLOOK_EMAIL = "virtru-challenge@outlook.com"
OUTLOOK_PASSWORD = "!nsecur3Pa$$word"
EMAIL_SUBJECT_NAME = "automated-emoji-test"

driver = webdriver.Firefox()
driver.maximize_window()
driver.get('https://outlook.live.com/owa/')

email_content = 'Sed dignissim netus arcu id egestas ultricies lacus etiam libero mattis augue sit risus, neque magna 🍺🍒💍🏰🎻🐄🐩🕘🍥📊🏯📋💟🎦 mauris facilisis vestibulum eleifend 🔁🐅🎮🐘 nec 🕧🔯👪👸🍕🏆 sit lacus pulvinar quisque morbi maecenas 🌏👠🌐🎲 🍃👡📙💫👅💣 🔚🔞🐊🌗🐾📍🏤🎈💙 mattis suspendisse eu euismod 🍨🎻🍓🕘🏡📤👈🎊🍤📦. Sit ante maecenas pellentesque nibh dignissim amet eget sit sed nulla 🍢🔋🎾🎻🍆🌁🐹🎵🐗🔭 feugiat orci ipsum viverra sit orci condimentum ultricies leo diam orci et orci, nec quam blandit. 🍁🔴🏰🎤💵🌖📔🍤🍈👅👾📕👉🌑 🎿🌶🍒🍸🏧🔤🍸🌒👌🔎💓🍩📌💗 vestibulum vitae dui pellentesque lobortis et sit id pellentesque diam at 🌼👒🗽🎉🔞💒💃👋🌳📡🍋🕜🐭🌻 ipsum convallis dapibus urna faucibus integer cras 🐏🔨🐲🌗🕣👐💠 aenean sed molestie semper a aliquet magna interdum et luctus quis commodo, felis est porttitor commodo.'

ms_doughboy_xpath = "//*[@class='o365cs-mfp-header']//div[@class='o365cs-mfp-doughboy-container']"


def sign_in(email, password):
    outlook_sign_in_xpath = "//*[@class='linkButtonFixedHeader office-signIn']"
    selenium_helpers.click_element_by_xpath(
        driver, outlook_sign_in_xpath, 2)

    email_input_xpath = "//input[@type='email']"
    selenium_helpers.send_keys_to_element_by_xpath(
        driver, email_input_xpath, email, 2)

    email_submit_button_xpath = "//input[@type='submit'][@value='Next']"
    selenium_helpers.click_element_by_xpath(
        driver, email_submit_button_xpath, 1)

    email_password_input_xpath = "//input[@type='password']"
    selenium_helpers.send_keys_to_element_by_xpath(
        driver, email_password_input_xpath, password, 2)

    password_submit_button_xpath = "//input[@type='submit'][@value='Sign in']"
    selenium_helpers.click_element_by_xpath(
        driver, password_submit_button_xpath, 2)

    # wait for successful sign in. Profile image(doughboy) loads late
    selenium_helpers.find_clickable_element_by_xpath(
        driver, ms_doughboy_xpath, 15)


def open_latest_email_with_subject(subject):
    email_with_subject_xpath = "//div[@aria-label='Mail list']//span[@class='lvHighlightAllClass lvHighlightSubjectClass'][text()[contains(.,'" + \
        subject + "')]]"
    selenium_helpers.click_element_by_xpath(
        driver, email_with_subject_xpath, 15)


def click_virtru_unlock_message_link():

    unlock_message_link_xpath = "//a[starts-with(@href, 'https://secure.virtru.com/start/?')][text()[contains(.,'Unlock Message')]]"
    selenium_helpers.click_element_by_xpath(
        driver, unlock_message_link_xpath, 15)


def send_verification_email(email):
    verify_email_xpath = "//span[@class='userEmail'][text()[contains(.,'" + email + "')]]"
    selenium_helpers.click_element_by_xpath(
        driver, verify_email_xpath, 12)

    send_me_a_verification_email_xpath = "//a[@class='btn btn-lg auth-choice-btn sendEmailButton']"
    selenium_helpers.click_element_by_xpath(
        driver, send_me_a_verification_email_xpath, 10)


def process_verification_email(email):
        # refresh page to
    driver.refresh()
    selenium_helpers.find_clickable_element_by_xpath(
        driver, ms_doughboy_xpath, 15)
    selenium_helpers.click_element_by_xpath(
        driver, "//*[@role='menu']//span[@title='Other']", 5)
    driver.implicitly_wait(3)

    # this will locate the latest email from verify@virtru.com
    # wait is longest here to account for email server sluggishness
    virtru_verification_email_xpath = "//*[@class='lvHighlightAllClass lvHighlightFromClass'][text()[contains(.,'verify@virtru.com')]]"
    selenium_helpers.click_element_by_xpath(
        driver, virtru_verification_email_xpath, 30)

    verify_me_link_xpath = "//a[starts-with(@href, 'https://accounts.virtru.com/email-activation?linkId=')][text()[contains(.,'VERIFY ME')]]"
    selenium_helpers.click_element_by_xpath(
        driver, verify_me_link_xpath, 5)


def assert_email_contents(expected_email_contents):

    # ensure decrypt view has loaded
    encrypted_email_reply_input_xpath = "//div[@id='click-into-reply-view']"
    selenium_helpers.find_clickable_element_by_xpath(
        driver, encrypted_email_reply_input_xpath, 5)

    # get text from email body
    encrypted_email_body_xpath = "//*[@id='tdf-body']"
    encryped_email_body = selenium_helpers.find_clickable_element_by_xpath(
        driver, encrypted_email_body_xpath, 5)
    actual_email_contents = encryped_email_body.text
    # assert email text equal to expected_email_contents
    try:
        assert expected_email_contents == actual_email_contents
        print("Expected email contents are the same as actual email contents!")
    except AssertionError:
        print("Expected email contents are not the same as actual email contents! :(")
        print("Expected email contents: " + expected_email_contents)
        print("-------****-------")
        print("Actual email contents: "+ actual_email_contents)




sign_in(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
open_latest_email_with_subject(EMAIL_SUBJECT_NAME)
click_virtru_unlock_message_link()
driver.switch_to.window(driver.window_handles[1])
send_verification_email(OUTLOOK_EMAIL)
driver.switch_to.window(driver.window_handles[0])
process_verification_email(OUTLOOK_EMAIL)
driver.switch_to.window(driver.window_handles[1])
assert_email_contents(email_content)
driver.close()