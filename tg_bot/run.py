import asyncio, logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher()

# Хендлер с фильтром/класом CommandStart:
@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!')

@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')

@dp.message(F.text == 'Как дела?')
async def get_how(message: Message):
    await message.answer('Отлично!')

@dp.message(F.photo)
async def upload_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@dp.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAANZZoMVOOgAAcv0S4SguAuO4KxzY342AAIS4DEbTSsYSFB9fp1UB4-9AQADAgADeQADNQQ',
                               caption='Лежебока)))')
    
@dp.message(Command('love'))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://klike.net/uploads/posts/2023-01/1674457660_3-48.jpg',
                               caption='Вот что я люблю!)')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')