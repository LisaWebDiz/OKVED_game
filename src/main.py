import sys
from src.normalizer import PhoneNormalizer
from src.okved_fetcher import OkvedFetcher, flatten_okved_tree
from src.okved_matcher import OkvedMatcher

# URL ежедневно обновляемого okved.json
RAW_URL = "https://raw.githubusercontent.com/bergstar/testcase/refs/heads/master/okved.json"


def main():
    # Проверка, что номер передан
    if len(sys.argv) < 2:
        print("Использование: python -m src.main \"номер телефона\"")
        sys.exit(1)

    input_number = sys.argv[1]

    # Нормализация номера
    normalizer = PhoneNormalizer()
    normalized = normalizer.normalize(input_number)

    if normalized is False:
        print("Ошибка: невалидный номер")
        sys.exit(1)

    print(f"Нормализованный номер: {normalized}")

    # Загрузка ОКВЭД
    try:
        fetcher = OkvedFetcher(RAW_URL)
        raw_data = fetcher.fetch()
        okved_data = flatten_okved_tree(raw_data)  # Преобразуем вложенную структуру в плоский список
    except Exception as e:
        print(f"Ошибка загрузки ОКВЭД: {e}")
        sys.exit(1)

    # Поиск всех совпадений с максимальной длиной
    matcher = OkvedMatcher(okved_data)
    results = matcher.find_best_matches(normalized)

    print("\n--- Результаты поиска ---")
    for r in results:
        print(f"Код ОКВЭД: {r['code']}")
        print(f"Название: {r['name']}")
        print(f"Длина совпадения: {r['match_length']}")
        print("---")


if __name__ == "__main__":
    main()
