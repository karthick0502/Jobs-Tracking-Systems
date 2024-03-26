from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login_LinkedIn(browser, User, Password, Feed, Applied):
    try:
        driver = browser
        # Enter login credentials and submit
        driver.find_element(By.ID, value='username').send_keys(User)
        driver.find_element(By.ID, value='password').send_keys(Password)
        driver.find_element(By.CLASS_NAME, value="login__form_action_container ").click()
        driver.implicitly_wait(2)
        while True:
            try:
                WebDriverWait(driver, 10).until(EC.url_changes(Feed))
            except Exception:
                pass
            if driver.current_url == Feed:
                break
        # driver.implicitly_wait(10)
        driver.get(Applied)
        driver.implicitly_wait(2)
        return driver
    except Exception as e:
        raise e
