from aiogram.utils import executor
from create_bot import dp
from database import sqlite_db


async def on_startup(_):    #Что происходит при создании бота
    print('Bot online')
    sqlite_db.sql_start() #При старте бота произойдет запуск нашей БД

from handlers import client, admin, other   #Импорт

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)   #Должен быть последний
    
executor.start_polling(dp, skip_updates = True, on_startup=on_startup)   #Начало работы skip_updates - Пропуск обнов on_startup - Что делать при запуске вызов верхней функции
