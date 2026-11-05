import random
import string

def generate_email(prefix: str = "test", cohort: int = 1999) -> str:
    random_chars = ''.join(random.choices(string.ascii_lowercase, k=3))
    random_digits = ''.join(random.choices(string.digits, k=3))
    return f"{prefix}{random_chars}{cohort}{random_digits}@yandex.ru"

def generate_password(length: int = 8) -> str:
    if length < 1:
        raise ValueError("Длина пароля должна быть не меньше 1")
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))