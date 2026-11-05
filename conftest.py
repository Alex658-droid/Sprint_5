import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils.locators import (
    LOCATOR_LOGIN_INPUT_EMAIL,
    LOCATOR_LOGIN_INPUT_PASSWORD,
    LOCATOR_LOGIN_BUTTON,
    LOCATOR_BTN_PERSONAL_CABINET,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://stellarburgers.education-services.ru"


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


@pytest.fixture
def base_url():
    return BASE_URL


# ==================== ДАННЫЕ ДЛЯ РЕГИСТРАЦИИ ====================

@pytest.fixture
def name():
    return "TestUser"


@pytest.fixture
def email():
    import random
    return f"test_user_{random.randint(1000, 99999)}@yandex.ru"


@pytest.fixture
def password():
    return "Pass1234"


@pytest.fixture
def short_password():
    return "123"


@pytest.fixture
def expected_error_text():
    return "Пароль должен содержать"


# ==================== ФИКСТУРА АВТОРИЗОВАННОГО ДРАЙВЕРА ====================

@pytest.fixture
def logged_in_driver(driver, base_url):
    logger.info("Выполняем вход через фикстуру logged_in_driver")
    driver.get(base_url + "/login")
    wait = WebDriverWait(driver, 30)

    # 1. Ждем отрисовки формы (заголовок "Вход")
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='Вход']")))

    # 2. Находим элементы
    email_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_EMAIL))
    password_field = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_INPUT_PASSWORD))
    login_btn = wait.until(EC.presence_of_element_located(LOCATOR_LOGIN_BUTTON))

    # 3. Ввод данных (обязательно подставь СВОИ реальные email и пароль)
    email_field.click()
    email_field.clear()
    email_field.send_keys("sentestov2000@yandex.ru")   # <-- ВСТАВЬ СЮДА СВОЙ EMAIL

    password_field.click()
    password_field.clear()
    password_field.send_keys("1234567890")          # <-- ВСТАВЬ СЮДА СВОЙ ПАРОЛЬ

    # 4. Клик по кнопке через JS (обходит перекрывающие слои)
    driver.execute_script("arguments[0].click();", login_btn)

    # 5. Ждем появления «Личный Кабинет» в шапке — признак успешного входа
    wait.until(EC.presence_of_element_located(LOCATOR_BTN_PERSONAL_CABINET))

    logger.info("Вход выполнен успешно")
    return driver