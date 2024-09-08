import os
import asyncio, logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from app.handlers import router                 # Импортируем маршрутизатор из handlers.py

# Асинхронная функция, которая запускает бота
async def main():
    load_dotenv()                               # Загружаем переменные окружения из файла .env
    bot = Bot(token = os.getenv('TG_TOKEN'))    # Инициализируем объект бота с токеном, полученным из переменной окружения
    dp = Dispatcher()                           # Создаем диспетчер, который управляет маршрутизацией и обработкой сообщений
    dp.include_router(router)                   # Включаем маршрутизатор из handlers.py в диспетчер
    await dp.start_polling(bot)                 # Запускаем бесконечный цикл для обработки входящих сообщений

# Основной блок кода, который запускается при выполнении скрипта
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)     # Базовое логирование с уровнем INFO (ТОЛЬКО ДЛЯ ОТЛАДКИ ПРОЦЕССА!)
    try:
        asyncio.run(main())                     # Запускаем асинхронную функцию main с помощью asyncio.run
    except KeyboardInterrupt:
        print('Бот отключен')                   # Если запуск не успешен, выводится сообщение 'Бот отключен'