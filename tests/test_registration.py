import logging
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from utils.data import BASE_URL, NAME
from utils.locators import (
    LOCATOR_REGISTRATION_HEADER,
    LOCATOR_REG_INPUT_NAME,
    LOCATOR_REG_INPUT_EMAIL,
    LOCATOR_REG_INPUT_PASSWORD,
    LOCATOR_REG_BUTTON,
    LOCATOR_ERROR_MESSAGE,
)

logger = logging.getLogger(__name__)


class TestRegistration:

    @pytest.mark.parametrize("password", ["Pass1234"])
    def test_registration_success(self, driver, password):
        # Уникальный email на каждый прогон — иначе при повторном запуске
        # сервер ответит «пользователь уже существует» и тест упадёт
        email = f"valid_test_{int(time.time())}@ya.ru"

        driver.get(BASE_URL + "/register")
        wait = WebDriverWait(driver, 30)

        wait.until(EC.visibility_of_element_located(LOCATOR_REGISTRATION_HEADER))

        name_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_NAME))
        email_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_EMAIL))
        pass_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_PASSWORD))
        reg_btn = wait.until(EC.presence_of_element_located(LOCATOR_REG_BUTTON))

        name_field.click()
        name_field.send_keys(NAME)

        email_field.click()
        email_field.send_keys(email)

        pass_field.click()
        pass_field.send_keys(password)
        # Уводим фокус, чтобы React зафиксировал ввод и отработал валидацию
        pass_field.send_keys(Keys.TAB)

        driver.execute_script("arguments[0].click();", reg_btn)

        try:
            # После успешной регистрации — редирект на страницу входа
            wait.until(lambda d: "login" in d.current_url.lower())
        except TimeoutException:
            logger.error(f"Регистрация не удалась. URL: {driver.current_url}")
            logger.error(f"Email: {email}")
            for el in driver.find_elements(By.CSS_SELECTOR, "p.input__error"):
                if el.text.strip():
                    logger.error(f"Ошибка на странице: {el.text!r}")
            raise

        assert "/login" in driver.current_url.lower()

    @pytest.mark.parametrize("short_password,expected_error_text", [
        ("short", "Некорректный пароль"),
        ("12345", "Некорректный пароль"),
    ])
    def test_registration_invalid_password(self, driver, short_password, expected_error_text):
        # Email тоже делаем уникальным, чтобы валидация пароля срабатывала,
        # а не «пользователь уже существует»
        email = f"short_pass_{int(time.time())}_{short_password}@ya.ru"

        driver.get(BASE_URL + "/register")
        wait = WebDriverWait(driver, 30)

        wait.until(EC.visibility_of_element_located(LOCATOR_REGISTRATION_HEADER))

        name_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_NAME))
        email_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_EMAIL))
        pass_field = wait.until(EC.presence_of_element_located(LOCATOR_REG_INPUT_PASSWORD))
        reg_btn = wait.until(EC.presence_of_element_located(LOCATOR_REG_BUTTON))

        name_field.click()
        name_field.send_keys(NAME)

        email_field.click()
        email_field.send_keys(email)

        pass_field.click()
        pass_field.send_keys(short_password)
        # Уводим фокус, чтобы React зафиксировал ввод и отработал валидацию
        pass_field.send_keys(Keys.TAB)

        driver.execute_script("arguments[0].click();", reg_btn)

        err_el = wait.until(EC.visibility_of_element_located(LOCATOR_ERROR_MESSAGE))
        assert expected_error_text in err_el.text