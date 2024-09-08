import os, uuid, json
import aiohttp  # Импортируем aiohttp для выполнения асинхронных HTTP-запросов

from utils import get_file_id # Импортируем регулярное выражение

# Асинхронная функция для получения токена доступа
async def get_access_token() -> str:
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"   # URL для запроса токена

    payload = {"scope": "GIGACHAT_API_PERS"}                    # Тело запроса
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),                             # Уникальный идентификатор запроса
    }
    
    # Используем aiohttp для выполнения POST-запроса с базовой аутентификацией
    auth = aiohttp.BasicAuth(os.getenv('ID_CLIENT_SBER'), 
                             os.getenv('AI_SECRET_SBER'))
    # Создаем асинхронную HTTP-сессию с использованием базовой аутентификации
    async with aiohttp.ClientSession(auth=auth) as session:
        # Отправляем POST-запрос на получение токена доступа
        async with session.post(url, 
                                headers = headers, 
                                data = payload, 
                                ssl = False) as res:
            response = await res.json()                         # Асинхронно парсим JSON-ответ от сервера
            access_token = response["access_token"]             # Извлекаем токен доступа из ответа
            return access_token                                 # Возвращаем токен

# Асинхронная функция для отправки текста на сервер и получения текстового ответа
async def send_prompt(msg: str, access_token: str):
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"    # URL для отправки сообщений

    payload = {
        "model": "GigaChat-Pro",    # Указываем модель для генерации ответа
        "messages": [
            {
                "role": "user",
                "content": msg, # Сообщение пользователя
            }
        ],
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'   # Токен доступа в заголовке Authorization
    }

    # Асинхронно выполняем POST-запрос с сообщением пользователя
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload, ssl=False) as response:
            response_json = await response.json()                       # Парсим JSON-ответ от сервера
            return response_json["choices"][0]["message"]["content"]    # Возвращаем содержимое ответа

# Асинхронная функция для отправки текста на сервер и получения картинки
async def get_image(file_id: str, access_token: str):
    url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{file_id}/content"

    headers = {
        'Accept': 'application/jpg',
        'Authorization': f'Bearer {access_token}'
    }

    # Создаем асинхронную сессию для выполнения запроса
    async with aiohttp.ClientSession() as session:
        # Асинхронно выполняем GET-запрос
        async with session.get(url, headers=headers, ssl=False) as response:
            # Читаем содержимое ответа как байты
            return await response.read()
        
async def sent_prompt_and_get_response(msg: str, access_token: str):
    # Асинхронно отправляем запрос и получаем ответ
    res = await send_prompt(msg, access_token)
    
    # Получаем идентификатор файла и флаг, указывающий, является ли это изображением
    data, is_image = get_file_id(res)  # get_file_id можно оставить синхронной, так как она не требует ввода-вывода
    
    # Если это изображение, асинхронно получаем его содержимое
    if is_image:
        data = await get_image(file_id=data, access_token=access_token)
    
    # Возвращаем данные и флаг, указывающий, является ли это изображением
    return data, is_image