import json
from datetime import date
from pathlib import Path
from typing import List, Dict, Union

import requests


class OkvedFetcher:
    """
    Класс для загрузки okved.json по HTTPS с файловым кэшем
    или из локального файла
    """

    def __init__(self, url: str):
        """
        :param url: URL к JSON-файлу или путь к локальному файлу
        """
        self.url = url

        # Настройки кэша (используются только для HTTP)
        self.cache_dir = Path("cache")
        self.cache_file = self.cache_dir / "okved.json"
        self.meta_file = self.cache_dir / "cache_meta.json"

    def _is_cache_valid(self) -> bool:
        if not self.cache_file.exists() or not self.meta_file.exists():
            return False

        try:
            meta = json.loads(self.meta_file.read_text(encoding="utf-8"))
            return meta.get("cache_date") == date.today().isoformat()
        except (json.JSONDecodeError, OSError):
            return False

    def _load_cache(self) -> Union[List[Dict], Dict]:
        """
        Загрузка данных из кэша
        """
        return json.loads(self.cache_file.read_text(encoding="utf-8"))

    def _save_cache(self, data: Union[List[Dict], Dict]) -> None:
        """
        Сохранение данных и мета-информации в кэш
        """
        self.cache_dir.mkdir(exist_ok=True)

        self.cache_file.write_text(
            json.dumps(data, ensure_ascii=False),
            encoding="utf-8"
        )
        self.meta_file.write_text(
            json.dumps({"cache_date": date.today().isoformat()}),
            encoding="utf-8"
        )

    def fetch(self) -> Union[List[Dict], Dict]:
        """
        Загрузка okved.json:
        - из локального файла, если url не http
        - из кэша, если он актуален
        - по HTTPS с обновлением кэша
        """
        try:
            # Локальный файл — без кэша
            if not self.url.startswith("http"):
                with open(self.url, encoding="utf-8") as f:
                    return json.load(f)

            # HTTP + актуальный кэш
            if self._is_cache_valid():
                return self._load_cache()

            # Попытка скачивания
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()
            data = response.json()

            self._save_cache(data)
            return data

        except (requests.RequestException, json.JSONDecodeError, OSError) as e:
            # Fallback: использования старого кэша, если он есть
            if self.cache_file.exists():
                return self._load_cache()

            raise RuntimeError(f"Не удалось загрузить okved.json: {e}")


def flatten_okved_tree(tree: List[Dict]) -> List[Dict]:
    """
    Преобразует вложенное дерево ОКВЭД в плоский список словарей
    с ключами 'code' и 'name'
    """
    flat_list = []
    for node in tree:
        if "code" in node and "name" in node:
            flat_list.append({
                "code": node["code"],
                "name": node["name"]
            })
        if "items" in node and isinstance(node["items"], list):
            flat_list.extend(flatten_okved_tree(node["items"]))
    return flat_list
