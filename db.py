from aiogram.types import ParseMode
from aiogram import utils
from peewee import *

#Создание базы данных
db = SqliteDatabase('laptop.db')
CountQuantity = 0

#Базовый класс
class BaseModel(Model):
    class Meta:
        database = db

#Таблица с найденными ссылками
class Laptop(BaseModel):
    title = CharField() #Ключевое слово, заданное пользователем
    url = TextField() #Ссылка на объект

#Таблица с ключевыми словами и Id чата с пользователями
class SearchModel(BaseModel):
    title = CharField() #Ключевое слово, заданное пользователем
    chatid = CharField() #Id чата
    intid = IntegerField() # Храним номер запроса, чтобы потом иметь доступ к последнему запросу

#Функция, выдающая полный список найденных ссылок
def find_all_laptops():
    return Laptop.select()

#Функция, возвращающая ключевые слова, заданные пользователем
def find_id_search(chat_id):
    return SearchModel.select().where(SearchModel.chatid == chat_id)

#Функция, выдающая все найденные объекты
def find_all_search():
    return SearchModel.select()

#Функция, добавляющая и удаляющая ключевые слова из таблицы
async def process_search_model(message):
    global CountQuantity
    search_exist = True
    #Проверяем, существует ли данный объект в таблице
    try:
        search = SearchModel.select().where(SearchModel.title == message.text).get()
        search.delete_instance()
        await message.answer('Word {} was deleted'.format(message.text))
        return search_exist
    except DoesNotExist as de:
        search_exist = False
    #Если данного объекта нет, то добавляем его и выводим соответсвующее сообщение пользователю
    if not search_exist:
        rec = SearchModel(title = message.text, chatid = message.chat.id, intid = CountQuantity)
        rec.save()
        CountQuantity += 1
        await message.answer('Word {} was added'.format(message.text))
    return search_exist
# Функция, удаляющая последнее слово, введённое пользователем
async def delete_last_message(message):
    try:
        max_index = SearchModel.select(fn.Max(SearchModel.intid))
        last_message = SearchModel.select().where(SearchModel.intid == max_index).get()
        word = last_message.title
        last_message.delete_instance()
        await message.answer('Word {} was deleted'.format(word))
    except DoesNotExist:
        await message.answer('Please add new words!')


#Функция, добавляющая новые предложения в таблицу
async def process_laptops(title, url, chat_id, bot):
    laptop_exists = True
    try:
        laptop = Laptop.select().where(Laptop.title==title).get()
    except DoesNotExist as de:
        laptop_exists = False

    if not laptop_exists:
        rec = Laptop(title = title, url = url)
        rec.save()
        arr = title.split('\n')
        text_for_message = ''
        for i in arr:
            if i.find("Ноут")>=0:
                begin = 0
                end = 0
                while i[begin] != 'Н':
                    begin += 1
                while i[end] != ']':
                    end += 1
                end += 1
                text_for_message += i[begin:end]
        message_text = utils.markdown.hlink(text_for_message, url)
        await bot.send_message(chat_id=chat_id, text = message_text, parse_mode=ParseMode.HTML)

    return laptop_exists
#Инициализация базы данных
def init_db():
    db.create_tables([Laptop, SearchModel])


