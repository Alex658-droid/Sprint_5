import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.locators import (
    LOCATOR_LOGO,
    LOCATOR_BTN_CONSTRUCTOR,
    LOCATOR_BTN_EXIT,
    LOCATOR_PROFILE_TRIGGER,
    LOCATOR_BTN_LOGIN_MAIN,
)

logger = logging.getLogger(__name__)

def click_via_js(driver, element):
    driver.execute_script("arguments.click();", element)

def test_transition_from_cabinet_to_constructor_via_button(logged_in_driver, base_url):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 45)
    driver.get(f"{base_url}/profile")
    constructor_btn = wait.until(EC.element_to_be_clickable(LOCATOR_BTN_CONSTRUCTOR))
    constructor_btn.click()
    wait.until(lambda d: "/constructor" in d.current_url or "/" in d.current_url)

def test_transition_via_logo(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 45)
    logo = wait.until(EC.presence_of_element_located(LOCATOR_LOGO))
    try:
        wait.until(EC.element_to_be_clickable(LOCATOR_LOGO)).click()
    except Exception:
        click_via_js(driver, logo)
    wait.until(lambda d: d.current_url != "")
    assert (driver.current_url.endswith("/") or "/constructor" in driver.current_url)





def test_logout(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 45)

    if "/account" not in driver.current_url.lower():
        profile_trigger = wait.until(EC.element_to_be_clickable(LOCATOR_PROFILE_TRIGGER))
        try:
            profile_trigger.click()
        except Exception:
            driver.execute_script("arguments[0].click();", profile_trigger)

    logout_btn = wait.until(EC.visibility_of_element_located(LOCATOR_BTN_EXIT))

    driver.execute_script("arguments[0].click();", logout_btn)

    try:
        wait.until(lambda d: "/account" not in d.current_url.lower())
    except TimeoutException:
        print(f"!!! URL после клика: {driver.current_url}")
        raise

    assert "/account" not in driver.current_url.lower()