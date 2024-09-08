from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# Колбек клава:
main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Стас', callback_data='stas')],
    [InlineKeyboardButton(text='Марат', callback_data='marat'),
    InlineKeyboardButton(text='Роман', callback_data='roman')]
])
# Обычная клава:
# main = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text='Ежедневник 📔')],
#         [KeyboardButton(text='Фотосток 📸'), KeyboardButton(text='Ссылки 🌐')]
#     ],
#         resize_keyboard=True, # Для оптимизации высоты кнопок
#         input_field_placeholder='Выберите пункт в меню.' # Дополняет в строке ввода описание
# )

settings = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Добавить запись', url='https://www.notion.so/Activity-e0509978507d4aa4bbdeecbc4d380431'),
         InlineKeyboardButton(text='GitHub', url='https://github.com/ZOORoman')]
])

points = ['Мальдивы', 'Кавказ', 'Сочи', 'Хибины']

async def inline_points():
    keyboard = InlineKeyboardBuilder()
    for point in points:
        keyboard.add(InlineKeyboardButton(text=point, callback_data=f'point_{point}'))
    return keyboard.adjust(2).as_markup()