from src.okved_matcher import OkvedMatcher

# Пример данных ОКВЭД для теста
okved_data = [
    {"code": '07.2', 'name': 'Добыча руд цветных металлов'},
    {"code": '51.22', 'name': 'Деятельность космического транспорта'},
    {"code": '56', 'name': 'Деятельность по предоставлению продуктов питания и напитков'}
]

class TestOkvedMatcher:
    """
    Тест на совпадение последних цифр с ОКВЭД
    """

    def setup_method(self):
        """Создание объекта OkvedMatcher перед каждым тестом"""
        self.matcher = OkvedMatcher(okved_data)

    def test_full_suffix_match(self):
        """Тест на точное совпадение суффикса"""
        phone = '+07.2'
        results = self.matcher.find_best_matches(phone)
        assert len(results) == 1
        result = results[0]
        assert result['code'] == '07.2'
        assert result['match_length'] == len('072')

    def test_partial_suffix_match(self):
        """Тест на частичное совпадение суффикса"""
        phone = '+51.22'
        results = self.matcher.find_best_matches(phone)
        assert len(results) == 1
        result = results[0]
        assert result['code'] == '51.22'
        assert result['match_length'] == len('5122')

    def test_no_match_returns_default(self):
        """Тест резервной стратегии при отсутствии совпадений"""
        phone = "+9999"
        results = self.matcher.find_best_matches(phone)
        assert len(results) == 1
        result = results[0]
        assert result['code'] is None
        assert result['match_length'] == 0
        assert result['name'] == 'Совпадений не найдено'
