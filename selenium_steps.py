import selenium_helpers

MS_DOUGHBOY_XPATH = "//*[@class='o365cs-mfp-header']//div[@class='o365cs-mfp-doughboy-container']"
SHORT_WAIT = 5
MEDIUM_WAIT = 15
LONG_WAIT = 30

def sign_in(driver, email, password):
    outlook_sign_in_xpath = "//*[@class='linkButtonFixedHeader office-signIn']"
    selenium_helpers.click_element_by_xpath(
        driver, outlook_sign_in_xpath, SHORT_WAIT)

    email_input_xpath = "//input[@type='email']"
    selenium_helpers.send_keys_to_element_by_xpath(
        driver, email_input_xpath, email, SHORT_WAIT)

    email_submit_button_xpath = "//input[@type='submit'][@value='Next']"
    selenium_helpers.click_element_by_xpath(
        driver, email_submit_button_xpath, SHORT_WAIT)

    email_password_input_xpath = "//input[@type='password']"
    selenium_helpers.send_keys_to_element_by_xpath(
        driver, email_password_input_xpath, password, SHORT_WAIT)

    password_submit_button_xpath = "//input[@type='submit'][@value='Sign in']"
    selenium_helpers.click_element_by_xpath(
        driver, password_submit_button_xpath, SHORT_WAIT)

    """ wait for successful sign in.
    Profile image(doughboy) loads late
    """
    selenium_helpers.find_clickable_element_by_xpath(
        driver, MS_DOUGHBOY_XPATH, MEDIUM_WAIT)


def open_latest_email_with_subject(driver, subject):
    email_with_subject_xpath = "//div[@aria-label='Mail list']//span[@class='lvHighlightAllClass lvHighlightSubjectClass'][text()[contains(.,'" + \
        subject + "')]]"
    selenium_helpers.click_element_by_xpath(
        driver, email_with_subject_xpath, MEDIUM_WAIT)


def click_virtru_unlock_message_link(driver):

    unlock_message_link_xpath = "//a[starts-with(@href, 'https://secure.virtru.com/start/?')][text()[contains(.,'Unlock Message')]]"
    selenium_helpers.click_element_by_xpath(
        driver, unlock_message_link_xpath, 15)


def send_verification_email(driver, email):
    verify_email_xpath = "//span[@class='userEmail'][text()[contains(.,'" + email + "')]]"
    selenium_helpers.click_element_by_xpath(
        driver, verify_email_xpath, MEDIUM_WAIT)

    send_me_a_verification_email_xpath = "//a[@class='btn btn-lg auth-choice-btn sendEmailButton']"
    selenium_helpers.click_element_by_xpath(
        driver, send_me_a_verification_email_xpath, MEDIUM_WAIT)


def process_verification_email(driver, email):
    """ Refresh page to avoid errors
    and give time for email to be received"""
    driver.refresh()
    selenium_helpers.find_clickable_element_by_xpath(
        driver, MS_DOUGHBOY_XPATH, MEDIUM_WAIT)

    """ Outlook filters verification emails into the Other folder"""
    selenium_helpers.click_element_by_xpath(
        driver, "//*[@role='menu']//span[@title='Other']", SHORT_WAIT)
    driver.implicitly_wait(3)

    """ this will locate the latest email from verify@virtru.com
    wait_time is longest here to account for email server sluggishness
    """
    virtru_verification_email_xpath = "//*[@class='lvHighlightAllClass lvHighlightFromClass'][text()[contains(.,'verify@virtru.com')]]"
    selenium_helpers.click_element_by_xpath(
        driver, virtru_verification_email_xpath, LONG_WAIT)

    verify_me_link_xpath = "//a[starts-with(@href, 'https://accounts.virtru.com/email-activation?linkId=')][    text()[contains(.,'VERIFY ME')]]"
    selenium_helpers.click_element_by_xpath(
        driver, verify_me_link_xpath, SHORT_WAIT)


def return_decrypted_email_contents(driver):
    encrypted_email_reply_input_xpath = "//div[@id='click-into-reply-view']"
    selenium_helpers.find_clickable_element_by_xpath(
        driver, encrypted_email_reply_input_xpath, SHORT_WAIT)

    # get text from email body
    encrypted_email_body_xpath = "//*[@id='tdf-body']"
    encryped_email_body = selenium_helpers.find_clickable_element_by_xpath(
        driver, encrypted_email_body_xpath, SHORT_WAIT)
    actual_email_contents = encryped_email_body.text
    return actual_email_contents
