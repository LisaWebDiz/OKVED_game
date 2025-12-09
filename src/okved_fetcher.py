import json
import requests
from typing import List, Dict, Union

class OkvedFetcher:
    """
    Класс для загрузки okved.json по HTTPS или из локального файла
    """

    def __init__(self, url: str):
        """
        :param url: URL к JSON-файлу или путь к локальному файлу
        """
        self.url = url

    def fetch(self) -> Union[List[Dict], Dict]:
        """
        Загружает okved.json и возвращает данные как Python-структуру
        :return: dict или list с данными
        :raises: RuntimeError при проблемах с загрузкой
        """
        try:
            if self.url.startswith("http"):
                response = requests.get(self.url, timeout=5)
                response.raise_for_status()
                data = response.json()
            else:
                with open(self.url, encoding="utf-8") as f:
                    data = json.load(f)
            return data
        except (requests.RequestException, json.JSONDecodeError, FileNotFoundError) as e:
            raise RuntimeError(f"Не удалось загрузить okved.json: {e}")


def flatten_okved_tree(tree: List[Dict]) -> List[Dict]:
    """
    Преобразует вложенное дерево ОКВЭД в плоский список словарей с 'code' и 'name'
    :param tree: вложенное дерево ОКВЭД
    :return: плоский список словарей с ключами 'code' и 'name'
    """
    flat_list = []
    for node in tree:
        if "code" in node and "name" in node:
            flat_list.append({"code": node["code"], "name": node["name"]})
        if "items" in node and isinstance(node["items"], list):
            flat_list.extend(flatten_okved_tree(node["items"]))
    return flat_list
