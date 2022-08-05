import time
import secrets
from selenium.webdriver.common.by import By


# Start the web browser, and log in to Schoology
def login(browser):

    browser.get("https://osseo.schoology.com/users/manage/edit/moreinfo")

    # Locate Username Box
    userName = browser.find_element(By.ID,"edit-mail")

    userName.send_keys(secrets.username)

    time.sleep(0.1) # delay for more reliablity

    # Locate Password Box
    passwordBox = browser.find_element(By.ID,'edit-pass')

    passwordBox.send_keys(secrets.password)

    browser.find_element(By.CLASS_NAME,'submit-span-wrapper')  # find log in button

    elem = browser.find_element(By.CLASS_NAME,'submit-span-wrapper')

    elem.click()  # click log in button

    print("Login Finished\n")
    time.sleep(6)  # delay for more reliablitiy