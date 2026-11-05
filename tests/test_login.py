import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.locators import (
    LOCATOR_BTN_LOGIN_MAIN,
    LOCATOR_BTN_PERSONAL_CABINET,
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_LOGIN_TITLE,
)


@pytest.mark.parametrize("scenario,locator", [
    ("Главная: кнопка «Войти в аккаунт»", LOCATOR_BTN_LOGIN_MAIN),
    ("Шапка: ссылка «Личный Кабинет»", LOCATOR_BTN_PERSONAL_CABINET),
])
def test_login_via_different_buttons(driver, base_url, scenario, locator):
    driver.get(base_url)
    wait = WebDriverWait(driver, 30)

    # 1. Кликаем по точке входа
    btn = wait.until(EC.element_to_be_clickable(locator))
    btn.click()

    # 2. Для неавторизованного пользователя обе точки ведут на /login
    wait.until(lambda d: "/login" in d.current_url)

    # 3. Убеждаемся, что открылась форма входа
    wait.until(EC.visibility_of_element_located(LOCATOR_LOGIN_TITLE))
    wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_BUTTON))

    # 4. Логинимся (используй СВОИ реальные данные)
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "name")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "Пароль")))

    email_field.click()
    email_field.send_keys("sentestov2000@yandex.ru")   # <-- свой email

    password_field.click()
    password_field.send_keys("1234567890")            # <-- свой пароль

    login_btn = wait.until(EC.element_to_be_clickable(LOCATOR_LOGIN_BUTTON))
    driver.execute_script("arguments[0].click();", login_btn)

    # 5. Вход успешен, если мы ушли со страницы /login
    wait.until(lambda d: "/login" not in d.current_url)