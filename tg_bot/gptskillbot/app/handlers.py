from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.api_sber import get_access_token, send_prompt, sent_prompt_and_get_response # Импортируем функции для работы с API

# Определяем группу состояний для конечного автомата состояний (FSM)
class Generate(StatesGroup):
    text = State()                                                  # Состояние, в котором бот ожидает текст от пользователя

router = Router()                                                   # Создаем объект маршрутизатора

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Приветствую! 🎉 \nЧем могу помочь?')
    await state.clear() # Очищаем текущее состояние FSM

# Обработчик текстовых сообщений
@router.message(F.text)
async def generate(message: Message, state: FSMContext):
    await state.set_state(Generate.text)  # Устанавливаем состояние, в котором бот ждет ответа
    access_token = await get_access_token()  # Асинхронно получаем токен доступа для API
    
    response, is_image = await sent_prompt_and_get_response(message.text, access_token)  # Отправляем текст пользователя на сервер и получаем ответ
    
    if is_image:
        await message.answer_photo(photo=response)  # Отправляем полученный ответ пользователю как фото
    else:
        await message.answer(response)  # Отправляем полученный ответ пользователю как текст
    await state.clear()  # Очищаем состояние FSM после отправки ответа
    
# Обработчик текстовых сообщений
# @router.message(F.text)
# async def generate(message: Message, state: FSMContext):
#     await state.set_state(Generate.text)  # Устанавливаем состояние, в котором бот ждет ответа
#     access_token = await get_access_token()  # Асинхронно получаем токен доступа для API
#     response = await send_prompt(message.text, access_token)  # Отправляем текст пользователя на сервер и получаем ответ
#     await message.answer(response)  # Отправляем полученный ответ пользователю
#     await state.clear()  # Очищаем состояние FSM после отправки ответа

# Обработчик повторных сообщений, пока бот обрабатывает запрос
@router.message(Generate.text)
async def generate_error(message: Message):
    await message.answer("Подождите, ответ генерируется...")        # Сообщаем пользователю, что ответ еще формируется
