import re

class OkvedMatcher:
    """
    Класс для поиска всех кодов ОКВЭД с максимальным совпадением по окончанию номера
    """

    def __init__(self, okved_data, default_code=None, default_name=None):
        """
        :param okved_data: список словарей с ключами 'code' и 'name'
        :param default_code: резервный код ОКВЭД, если совпадений нет
        :param default_name: резервное название
        """
        self.okved_data = okved_data
        self.default_code = default_code
        self.default_name = default_name

    def find_best_matches(self, phone_number):
        """
        Возвращает список всех ОКВЭД с максимальной длиной совпадения
        :param phone_number: нормализованный номер в формате +79XXXXXXXXX
        :return: список словарей с ключами 'code', 'name', 'match_length'
        """
        max_length = 0
        matches = []

        # Очищение номера от любых нецифровых символов
        number_digits = re.sub(r'\D', '', phone_number)

        for item in self.okved_data:
            code_digits = re.sub(r'\D', '', str(item.get('code', '')))
            name = item.get('name', '')

            if not code_digits:
                continue  # разделы без цифр пропускаются

            # Проверка: совпадает ли конец номера с кодом
            if number_digits.endswith(code_digits):
                match_len = len(code_digits)
                if match_len > max_length:
                    # Более длинное совпадение - сброс предыдущих
                    max_length = match_len
                    matches = [{"code": item['code'], "name": name, "match_length": match_len}]
                elif match_len == max_length:
                    # Добавление в случае совпадения длины
                    matches.append({"code": item['code'], "name": name, "match_length": match_len})

        # Резервная стратегия: если совпадений нет
        if not matches:
            matches = [{
                "code": self.default_code,
                "name": self.default_name if self.default_name else "Совпадений не найдено",
                "match_length": 0
            }]

        return matches
