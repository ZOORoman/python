from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.middlewares import TestMiddleware
router = Router()

router.message.outer_middleware(TestMiddleware())

class Reg(StatesGroup):
    name = State()
    number = State()

# Хендлер с фильтром/класом CommandStart:
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.username}!\nТвой ID: {message.from_user.id}\n')
    await message.reply(f'Имя: {message.from_user.first_name}\nФамилия: {message.from_user.last_name}\nПремиум: {message.from_user.is_premium}',
                         reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('Это команда /help')
    # await message.reply(reply_markup=await kb.inline_points())

@router.message(F.text == 'Как дела?')
async def get_how(message: Message):
    await message.answer('Отлично!')

@router.message(F.photo)
async def upload_photo(message: Message):
    await message.answer(f'ID фото: {message.photo[-1].file_id}')

@router.message(Command('get_photo'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAANZZoMVOOgAAcv0S4SguAuO4KxzY342AAIS4DEbTSsYSFB9fp1UB4-9AQADAgADeQADNQQ',
                               caption='Лежебока)))')
    
@router.message(Command('get_mount'))
async def get_photo(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAN2ZrdDV_FDVEBAUoTPWkvR11Kiuv4AAtjfMRvntbhJtzYHIa4P4o0BAAMCAAN5AAM1BA',
                               caption='Горы')
    
@router.message(Command('get_mount2'))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://get.wallhere.com/photo/landscape-mountains-lake-nature-reflection-grass-sky-river-national-park-valley-wilderness-Alps-tree-autumn-leaf-mountain-season-tarn-loch-mountainous-landforms-mountain-range-590185.jpg',
                               caption='Горы')
    
@router.message(Command('get_love'))
async def get_photo(message: Message):
    await message.answer_photo(photo='https://klike.net/uploads/posts/2023-01/1674457660_3-48.jpg',
                               caption='Вот что я люблю!)')
    
@router.callback_query(F.data == 'stas')
async def stas(callback: CallbackQuery):
    await callback.answer('Вы выбрали Стаса!', show_alert=True) # ТГ не видит что ответили callback, чтобы кнопки не светились прописали это 
    await callback.message.edit_text('Куда поедет Стас?', reply_markup=await kb.inline_points())

@router.message(Command('reg'))
async def reg_first(message: Message, state: FSMContext):
    await state.set_state(Reg.name)
    await message.answer('Введите Ваше имя:')

@router.message(Reg.name)
async def reg_second(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer('Введите свой телефон:')

@router.message(Reg.number)
async def reg_three(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Спасибо, регистрация завершена! \nИмя: {data["name"]}\nНомер: {data["number"]}\n ')
    await state.clear()