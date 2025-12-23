

class PhoneNormalizer:
    """
    Класс для нормализаци и мобильного номера
    """

    def normalize(self, phone_number: str):
        if not phone_number or not isinstance(phone_number, str):
            return False

        # Удаление пробелов, дефисов, скобок
        clean = (
            phone_number.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        # Проверка на длину
        if len(clean) < 10 or len(clean) > 13:
            return False

        # Проверка на международный префикс выхода "00" в начале номера с длиной 13
        if len(clean) == 13:
            if not clean.startswith("00"):
                return False
            clean = clean[2:]  # удаление '00'

        # Проверка на международный формат +7ХХХХХХХХХХ - на '+' в начале номера с длиной 12
        if len(clean) == 12:
            if not clean.startswith("+7"):
                return False
            clean = clean[1:]  # удаление '+'

        # Проверка на '7' или '8' в начале номера с длиной 11
        if len(clean) == 11:
            if clean[0] not in ("7", "8"):
                return False
            clean = clean[1:]  # удаление '7' или '8'

        # Проверка на '9' в начале номера с длиной 10
        if len(clean) == 10:
            if clean[0] != "9":
                return False
            return f"+7{clean}"

        return False  # на всякий случай
