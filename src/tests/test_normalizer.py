import pytest
from src.normalizer import PhoneNormalizer


class TestPhoneNormalizer:
    """
    Тест для проверки нормализации номера телефона
    """

    @pytest.fixture
    def normalizer(self):
        return PhoneNormalizer()

    # валидные номера
    @pytest.mark.parametrize("raw, expected", [
        ("8 (999) 123-45-67", "+79991234567"),
        ("+7 (999) 123-45-67", "+79991234567"),
        ("+79991234567", "+79991234567"),
        ("89991234567", "+79991234567"),
        ("9991234567", "+79991234567"),
        (" 8 999 123 45 67 ", "+79991234567"),
    ])
    def test_valid_numbers(self, normalizer, raw, expected):
        assert normalizer.normalize(raw) == expected

    # невалидные номера
    @pytest.mark.parametrize("raw", [
        "",               # пустая строка
        None,             # не строка
        "+7abc999d9999",  # буквы
        "+89991234567",   # '+8' — запрещено
        "+7999123456",    # 11 символов, но при '+7' должно быть 12 символов
        "7999123456",     # 10 цифр, но начинается не с '9'
        "69991234567",    # 11 цифр, но начинается не с '7' или '8'
        "999123456",      # мало цифр
        "99912345678",    # 11 цифр, но начинается с '9'
    ])
    def test_invalid_numbers(self, normalizer, raw):
        assert normalizer.normalize(raw) is False
