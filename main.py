import logging
import asyncio
import telebot
import aiogram
from aiogram import Bot, Dispatcher, executor, utils, types
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton
from db import process_search_model, init_db, find_id_search, find_all_laptops
from parser_ import ParseLaptop

from config import TOKEN, URL, XPATH

logging.basicConfig(level=logging.INFO)


#Создание бота
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

#Создание клавиатуры
b1 = KeyboardButton('/search')
keyboard = aiogram.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(b1)

#Начало работы с telegram bot
@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Hello!", reply_markup=keyboard)

#Функция обработки ключевых слов поиска
@dp.message_handler(commands = 'requests')
async def send_search(message: types.Message):
    search_models = find_id_search(message.chat.id)
    for search_model in search_models:
        await message.answer(text=search_model.title)

#Функция запуска парсинга
@dp.message_handler(commands = 'search')
async def scheduled (message: types.Message):
    laptops = find_all_laptops()
    for laptop in laptops:
        laptop.delete_instance()
    await parser.parse()


#Функция, возвращающая все введённые пользователем ключевые слова
@dp.message_handler()
async def echo(message: types.Message):
    if message.text != '/start' and message.text != '/search':
        await process_search_model(message)


#Запуск telegram бота
if __name__ =='__main__':
    init_db()
    parser = ParseLaptop(url=URL,xpath=XPATH, bot = bot)
    executor.start_polling(dp, skip_updates=True)

