import re
from typing import Any

# Функция которая позволяет достать содержимое из атрибута src
def get_file_id(data: str) -> tuple[Any, bool]:
    print(data)
    # Поиск регулярного выражения в данных
    match = re.search(r'src="([^"]+)"', data)
    if match:
        return match.group(1), True # Возвращаем найденное значение и True
    else:
        return data, False # Возвращаем исходные данные и False