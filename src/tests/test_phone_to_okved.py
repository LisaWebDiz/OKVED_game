import pytest
from src.normalizer import PhoneNormalizer
from src.okved_matcher import OkvedMatcher

# Пример данных ОКВЭД
okved_data = [
    {"code": "07.29.3", "name": "Добыча и обогащение алюминийсодержащего сырья"},
    {"code": "16.29.3", "name": "Производство химических продуктов"},
    {"code": "22.29.3", "name": "Производство резиновых изделий"},
    {"code": "28.29.3", "name": "Производство машин и оборудования"},
    {"code": "29.3",    "name": "Производство автотранспорта"},
    {"code": "56.29.3", "name": "Деятельность по предоставлению продуктов питания"}
]

class TestPhoneToOkvedFull:
    """
    Тест на совпадение вводимого номера телефона с ОКВЭД
    """

    def setup_method(self):
        self.normalizer = PhoneNormalizer()
        self.matcher = OkvedMatcher(okved_data)

    @pytest.mark.parametrize("input_phone,expected_codes", [
        # Невалидные номера (короткие, не проходят normalize)
        ("8 (999) 163-29-3", None),
        ("+7 916 56-29-3", None),
        ("8999163293", None),

        # Валидный номер с одним совпадением
        ("+7 916 1243-29-3", {"29.3"}),

        # Валидный номер, но совпадений нет - резервная стратегия
        ("+7 999 000 0000", {None}),

        # Невалидный номер с некорректной первой цифрой
        ("5 (999) 123-45-67", None),
    ])
    def test_full_flow(self, input_phone, expected_codes):
        normalized = self.normalizer.normalize(input_phone)

        # Номер не удалось нормализовать
        if normalized is False:
            print(f"Ошибка: {input_phone} невалидный номер")
            assert expected_codes is None
            return

        # Номер нормализован, поиск совпадений
        results = self.matcher.find_best_matches(normalized)
        result_codes = {r["code"] for r in results}

        assert result_codes == expected_codes
