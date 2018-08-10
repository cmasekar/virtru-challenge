from selenium import webdriver
import selenium_steps

OUTLOOK_EMAIL = "virtru-challenge@outlook.com"
OUTLOOK_PASSWORD = "!nsecur3Pa$$word"
EMAIL_SUBJECT_NAME = "virtru-challenge-test"
EMAIL_CONTENT = 'Sed dignissim netus arcu id egestas ultricies lacus etiam libero mattis augue sit risus, neque magna 🍺🍒💍🏰🎻🐄🐩🕘🍥📊🏯📋💟🎦'


def initialize_webdriver():
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://outlook.live.com/owa/')
    return driver


def assert_email_contents(expected_email_contents, actual_email_contents):
    # assert email text equal to expected_email_contents
    try:
        assert expected_email_contents == actual_email_contents
        print("Expected email contents are the same as actual email contents!")
    except AssertionError:
        print(
            "Expected email contents are not the same as actual email contents! :(")
        print("Expected email contents: " + expected_email_contents)
        print("-------****-------")
        print("Actual email contents: " + actual_email_contents)


def virtru_test():

    driver = initialize_webdriver()

    selenium_steps.sign_in(driver, OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
    selenium_steps.open_latest_email_with_subject(driver, EMAIL_SUBJECT_NAME)
    selenium_steps.click_virtru_unlock_message_link(driver)

    # clicking unlock link opens up verification setup in new tab
    driver.switch_to.window(driver.window_handles[1])
    selenium_steps.send_verification_email(driver, OUTLOOK_EMAIL)

    # switching back to browser tab with email account
    driver.switch_to.window(driver.window_handles[0])
    selenium_steps.process_verification_email(driver, OUTLOOK_EMAIL)

    # verification link opens up in new tab
    driver.switch_to.window(driver.window_handles[1])

    decrypted_email_contents = selenium_steps.return_decrypted_email_contents(
        driver)
    assert_email_contents(EMAIL_CONTENT, decrypted_email_contents)

    #added for video recording purposes
    import time
    time.sleep(5)
    driver.close()


virtru_test()
