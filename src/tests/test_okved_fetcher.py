import pytest
from src.okved_fetcher import OkvedFetcher

class TestOkvedFetcher:
    """
    Класс-тест для проверки загрузки okved.json
    """

    URL = 'https://raw.githubusercontent.com/bergstar/testcase/refs/heads/master/okved.json'

    def setup_method(self):
        """Вызывается перед каждым тестом"""
        self.fetcher = OkvedFetcher(self.URL)

    def test_fetch_returns_data(self):
        """Проверка, что fetch возвращает данные"""
        data = self.fetcher.fetch()
        assert data is not None, 'Не удалось скачать данные'
        assert isinstance(data, (list, dict)), 'Данные должны быть list или dict'
