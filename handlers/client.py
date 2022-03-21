from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from database import sqlite_db

#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    try:
        await bot.send_message(message.from_user.id, "Hello", reply_markup=kb_client) #reply_markup - клавиатура
        await message.delete()
    except:
        await message.reply('Communicating with the bot via private messages ')

#@dp.message_handler(commands=['Working hours'])
async def command_open_time(message : types.Message):
    await bot.send_message(message.from_user.id, "Working hours (in code handlers/client.py Line 16)")
    await message.delete()

#@dp.message_handler(commands=['Address'])
async def command_place(message : types.Message):
    await bot.send_message(message.from_user.id, "Address (in code handlers/client.py Line 21)")
    await message.delete()

#@dp.message_handler(commands=['Assortment'])
async def command_menu(message : types.Message):
    await sqlite_db.sql_read(message) #Тут у нас связь с таблицей и в ней данные хранятся

def register_handlers_client(dp : Dispatcher):   #Функция в которую входят все прошллые созданные типы сообщений
    dp.register_message_handler(command_start, commands=['start', 'help']) #При каких условиях и какая функция врубится
    dp.register_message_handler(command_open_time, commands=['WorkingHours'])
    dp.register_message_handler(command_place, commands=['Address'])
    dp.register_message_handler(command_menu, commands=['Assortment'])