import random

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils.data import BASE_URL, EXISTING_EMAIL, EXISTING_PASSWORD
from utils.locators import (
    LOCATOR_LOGIN_INPUT_EMAIL,
    LOCATOR_LOGIN_INPUT_PASSWORD,
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_BTN_PERSONAL_CABINET,
    LOCATOR_LOGIN_HEADER,
)


# ==================== БАЗОВЫЕ ФИКСТУРЫ ====================

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    try:
        driver.quit()
    except Exception:
        pass


# ==================== ДИНАМИЧЕСКИЕ ТЕСТОВЫЕ ДАННЫЕ ====================

@pytest.fixture
def email():
    return f"test_user_{random.randint(1000, 99999)}@yandex.ru"


# ==================== ФИКСТУРА АВТОРИЗОВАННОГО ДРАЙВЕРА ====================

@pytest.fixture
def logged_in_driver(driver):
    driver.get(BASE_URL + "/login")
    wait = WebDriverWait(driver, 30)

    # 1. Ждем отрисовки формы (заголовок "Вход")
    wait.until(EC.visibility_of_element_located(LOCATOR_LOGIN_HEADER))

    # 2. Находим элементы
    email_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_EMAIL))
    password_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_PASSWORD))
    login_btn = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_BUTTON))

    # 3. Ввод данных
    email_field.click()
    email_field.clear()
    email_field.send_keys(EXISTING_EMAIL)

    password_field.click()
    password_field.clear()
    password_field.send_keys(EXISTING_PASSWORD)

    # 4. Клик по кнопке через JS (обходит перекрывающие слои)
    driver.execute_script("arguments[0].click();", login_btn)

    # 5. Ждем появления «Личный Кабинет» в шапке — признак успешного входа
    wait.until(EC.presence_of_element_located(LOCATOR_BTN_PERSONAL_CABINET))

    return driver