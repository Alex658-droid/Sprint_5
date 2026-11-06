import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.data import BASE_URL, EXISTING_EMAIL, EXISTING_PASSWORD
from utils.locators import (
    LOCATOR_BTN_LOGIN_MAIN,
    LOCATOR_BTN_PERSONAL_CABINET,
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_LOGIN_TITLE,
    LOCATOR_LOGIN_INPUT_EMAIL,
    LOCATOR_LOGIN_INPUT_PASSWORD,
)


@pytest.mark.parametrize("scenario,locator", [
    ("Главная: кнопка «Войти в аккаунт»", LOCATOR_BTN_LOGIN_MAIN),
    ("Шапка: ссылка «Личный Кабинет»", LOCATOR_BTN_PERSONAL_CABINET),
])
class TestLogin:

    def test_login_via_different_buttons(self, driver, scenario, locator):
        driver.get(BASE_URL)
        wait = WebDriverWait(driver, 30)

        # 1. Кликаем по точке входа
        btn = wait.until(EC.element_to_be_clickable(locator))
        btn.click()

        # 2. Для неавторизованного пользователя обе точки ведут на /login
        wait.until(lambda d: "/login" in d.current_url)

        # 3. Убеждаемся, что открылась форма входа
        wait.until(EC.visibility_of_element_located(LOCATOR_LOGIN_TITLE))
        wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_BUTTON))

        # 4. Логинимся данными из data-модуля
        email_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_EMAIL))
        password_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_PASSWORD))

        email_field.click()
        email_field.send_keys(EXISTING_EMAIL)

        password_field.click()
        password_field.send_keys(EXISTING_PASSWORD)

        login_btn = wait.until(EC.element_to_be_clickable(LOCATOR_LOGIN_BUTTON))
        driver.execute_script("arguments[0].click();", login_btn)

        # 5. Вход успешен, если мы ушли со страницы /login
        wait.until(lambda d: "/login" not in d.current_url)