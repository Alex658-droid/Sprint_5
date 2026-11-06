from selenium.webdriver.common.by import By

# ==================== АВТОРИЗАЦИЯ / ВХОД ====================

# Поле ввода e-mail (у него name='name')
LOCATOR_LOGIN_INPUT_EMAIL = (By.NAME, "name")

# Поле ввода пароля (name='Пароль')
LOCATOR_LOGIN_INPUT_PASSWORD = (By.NAME, "Пароль")

# Заголовок формы входа
LOCATOR_LOGIN_TITLE = (By.XPATH, "//h2[normalize-space()='Вход']")

# Кнопка «Войти» на форме входа
LOCATOR_LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")
LOCATOR_LOGIN_BTN_SUBMIT = LOCATOR_LOGIN_BUTTON  # алиас

# Кнопка «Войти в аккаунт» на главной
LOCATOR_BTN_LOGIN_MAIN = (By.XPATH, "//button[contains(normalize-space(), 'Войти в аккаунт')]")

# Ссылка «Войти» в шапке
LOCATOR_BTN_LOGIN_LINK = (By.XPATH, "//a[normalize-space()='Войти']")

# Пункт меню «Личный Кабинет» в шапке — это <a href="/account">
LOCATOR_BTN_PERSONAL_CABINET = (By.XPATH, "//a[normalize-space()='Личный Кабинет']")

# ==================== РЕГИСТРАЦИЯ ====================

# Поля: [0] Имя (name='name'), [1] Email (тоже name='name'!), [2] Пароль (name='Пароль')
LOCATOR_REG_INPUT_NAME = (By.XPATH, "(//input[@name='name'])[1]")
LOCATOR_REG_INPUT_EMAIL = (By.XPATH, "(//input[@name='name'])[2]")
LOCATOR_REG_INPUT_PASSWORD = (By.NAME, "Пароль")
LOCATOR_REG_BUTTON = (By.XPATH, "//button[normalize-space()='Зарегистрироваться']")
LOCATOR_REG_BTN_SUBMIT = LOCATOR_REG_BUTTON  # алиас

# Сообщение об ошибке валидации
LOCATOR_ERROR_MESSAGE = (By.XPATH,
    "//p[contains(text(), 'Некорректный пароль')] | "
    "//*[contains(@class, 'input__error')]"
)

# ==================== ЛИЧНЫЙ КАБИНЕТ / ЛОГАУТ ====================

# Кнопка «Конструктор» в шапке
LOCATOR_BTN_CONSTRUCTOR = (By.XPATH, "//a[normalize-space()='Конструктор']")

# Логотип (ссылка на главную)
LOCATOR_LOGO = (By.CSS_SELECTOR, "a[href='/']")

# Кнопка «Выход» в личном кабинете
LOCATOR_BTN_EXIT = (By.XPATH, "//button[normalize-space()='Выход']")

# Триггер профиля — пункт меню «Личный Кабинет» в шапке
LOCATOR_PROFILE_TRIGGER = LOCATOR_BTN_PERSONAL_CABINET

# Элемент профиля: имя пользователя или любая из ссылок личного кабинета.
# Используется в тесте логаута: после выхода элемент должен исчезнуть
LOCATOR_PROFILE_NAME = (By.XPATH,
    "//main//*[contains(@class, 'Account_profile')] | "
    "//main//a[normalize-space()='Профиль'] | "
    "//main//a[normalize-space()='История заказов'] | "
    "//main//button[normalize-space()='Выход']"
)

# ==================== ВКЛАДКИ КОНСТРУКТОРА ====================

# Вкладки — это div с классом tab_tab; активная имеет tab_tab_type_current
LOCATOR_TAB_BTN_BUNS = (By.XPATH, "//div[contains(@class, 'tab_tab')][normalize-space()='Булки']")
LOCATOR_TAB_BTN_SAUCES = (By.XPATH, "//div[contains(@class, 'tab_tab')][normalize-space()='Соусы']")
LOCATOR_TAB_BTN_FILLINGS = (By.XPATH, "//div[contains(@class, 'tab_tab')][normalize-space()='Начинки']")

# Карточка ингредиента (класс проверен дампом: BurgerIngredient_ingredient__1TVf6)
LOCATOR_INGREDIENT_CARD = (By.CSS_SELECTOR, "[class*='BurgerIngredient_ingredient__']")

LOCATOR_LOGIN_HEADER = (By.XPATH, "//h2[normalize-space()='Вход']")

LOCATOR_REGISTRATION_HEADER = (By.XPATH, "//h2[normalize-space()='Регистрация']")