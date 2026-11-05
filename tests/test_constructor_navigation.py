import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

from utils.locators import (
    LOCATOR_TAB_BTN_BUNS,
    LOCATOR_TAB_BTN_SAUCES,
    LOCATOR_TAB_BTN_FILLINGS,
    LOCATOR_INGREDIENT_CARD,
)


def wait_for_ingredients_loaded(driver, wait, locator):
    logger.info("Ждём появления карточек ингредиентов...")
    wait.until(EC.visibility_of_element_located(locator))
    logger.info("Карточки ингредиентов загружены.")


def tab_is_active(driver, locator):
    """Активная вкладка имеет класс tab_tab_type_current (или *_current у сегмента)."""
    cls = driver.find_element(*locator).get_attribute("class")
    return "current" in cls


def test_constructor_tabs_navigation(logged_in_driver, base_url):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 45)

    driver.get(f"{base_url}/")
    time.sleep(2)
    wait_for_ingredients_loaded(driver, wait, LOCATOR_INGREDIENT_CARD)

    # По умолчанию активна вкладка «Булки»
    bun_tab = wait.until(EC.element_to_be_clickable(LOCATOR_TAB_BTN_BUNS))
    assert bun_tab.is_displayed()
    assert tab_is_active(driver, LOCATOR_TAB_BTN_BUNS), "Вкладка «Булки» должна быть активной по умолчанию"

    # Переключаемся на «Соусы»
    sauce_tab = wait.until(EC.element_to_be_clickable(LOCATOR_TAB_BTN_SAUCES))
    sauce_tab.click()
    wait.until(lambda d: tab_is_active(d, LOCATOR_TAB_BTN_SAUCES))
    wait_for_ingredients_loaded(driver, wait, LOCATOR_INGREDIENT_CARD)

    # Переключаемся на «Начинки»
    filling_tab = wait.until(EC.element_to_be_clickable(LOCATOR_TAB_BTN_FILLINGS))
    filling_tab.click()
    wait.until(lambda d: tab_is_active(d, LOCATOR_TAB_BTN_FILLINGS))
    wait_for_ingredients_loaded(driver, wait, LOCATOR_INGREDIENT_CARD)
