import sqlite3 as sq
from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('data base.db') #Подключение к файлу базы данных, если его нет, то он создастся
    cur = base.cursor() #Отвечает за работу с БД
    if base:
        print('Data base connected') #Если подключились то в кмд выводится
    base.execute('CREATE TABLE IF NOT EXISTS menu (img TEXT, name TEXT PRIMARY KEY, description TEXT, price TEXT)') #Создать таблицу если такой не существует #4 столбца #img в тексте т.к фотки у нас по id
    base.commit()

async def sql_add_command(state):  #Принимаем наше состояние
    async with state.proxy() as data: #Открываем словарь
        cur.execute('INSERT INTO menu VALUES (?, ?, ?, ?)', tuple(data.values())) #Вставляем в таблицу значения по синтаксису sqlite в виде кортежа
        base.commit()
async def sql_read(message): #Получаем событие
    for ret in cur.execute('SELECT * FROM menu').fetchall(): #Выбрать все из таблицы menu в виде списка
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Description: {ret[2]}\n Price {ret[-1]}') #Отпарвляем по строке элементы списка

async def sql_read2():
    return cur.execute('SELECT * FROM menu').fetchall() #Просто для чтения и отсылки в handlers.admin py

async def sql_delete_command(data):
    cur.execute('DELETE FROM menu WHERE name == ?', (data,)) #Удалить по конкретному названию
    base.commit()