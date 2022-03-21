from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text
from database import sqlite_db
from keyboards import button_case_admin
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID_admin = None
class FSMAdmin(StatesGroup):  #Создали класс с 4 состояниями
    photo = State()
    name = State()
    description = State()
    price = State()
#Получение id текущего модератора для допуска
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)   #По команде moderator допуск, is_chat_admin - это админ чата? тогда допуск #Писать надо именно в группу, а не к боту
async def make_changes_command(message: types.Message):
    global ID_admin
    ID_admin = message.from_user.id #Как только админ заходит мы делаем ID глобальной и присваем айдишник админа
    await bot.send_message(message.from_user.id, 'Hello, Admin', reply_markup=button_case_admin) # И будет отправляться клавиатура админа еще #bot импортировать надо
    await message.delete()
#Начало диалога загрузки нового пункта меню
#@dp.message_handler(comands='Загрузить', state=None) #(Отправка в функцию def register_handlers_admin для последующей связи с файлом main)
async def cm_start(message:types.Message):
    if message.from_user.id == ID_admin: #Если пользователь занесен в ID админа то допуск
        await FSMAdmin.photo.set()  #Перевод бота в режим ожидания
        await message.reply('Upload product photo')


#Выход из состояний
#@dp.message_handler(state='*', commands='Отмена') #state='*' - В каком бы состоянии не находился бот на него это действует
#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*') #Text(....) - какой текст именно и ignore_case - игнорирует способы написания видимо можно большую букву ткнуть или что-то типа того
async def cancel_handler(message: types.message, state: FSMContext):
    if message.from_user.id == ID_admin:
        current_state = await state.get_state() #Ловим состояние бота
        if current_state is None:  #Если он не в состоянии, то мы от него отстаем
            return
        await state.finish()    #Ну тут просто финишнули и вывели его из всех состояний если он в них был
        await message.reply('OK')

#Ловим первый ответ и пишем в словарь
#@dp.message_handler(content_types=['photo'], state=FSMAdmin.photo) #(Отправка в функцию def register_handlers_admin для последующей связи с файлом main) #Благодаря FSMAdmin.photo бот понимает что именно сюда придет нужное фото
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID_admin:
        async with state.proxy() as data:  #открываем словарь
            data['photo'] = message.photo[0].file_id   #По ключу фото будет присвоен свой файл  и мы получаем id фото и пишем в словарь машинных состояний
        await FSMAdmin.next()    #Переводим бота в ожидание следующего ответа
        await message.reply('Enter the product name')

#Ловим второй ответ
#@dp.message_handler(state=FSMAdmin.name)#(Отправка в функцию def register_handlers_admin для последующей связи с файлом main) #Благодаря FSMAdmin.name бот понимает что именно сюда придет нужное имя
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID_admin:
        async with state.proxy() as data:  #открываем словарь
            data['name'] = message.text  #По ключу name будет присвоенно свое имя
        await FSMAdmin.next()    #Переводим бота в ожидание следующего ответа
        await message.reply('Enter a description')

#Ловим третий ответ
#@dp.message_handler(state=FSMAdmin.description)#(Отправка в функцию def register_handlers_admin для последующей связи с файлом main) #Благодаря FSMAdmin.description бот понимает что именно сюда придет нужное описание
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID_admin:
        async with state.proxy() as data:  #открываем словарь
            data['description'] = message.text  #По ключу name будет присвоенно свое описание
        await FSMAdmin.next()    #Переводим бота в ожидание следующего ответа
        await message.reply('Enter the price')

#Ловим четвертую ответ
#@dp.message_handler(state=FSMAdmin.price)#(Отправка в функцию def register_handlers_admin для последующей связи с файлом main) #Благодаря FSMAdmin.description бот понимает что именно сюда придет нужное описание
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID_admin:
        async with state.proxy() as data:  #открываем словарь
            data['price'] = float(message.text)  #Цена с плавающей точкой |надо поработать с ошибками со стороны админа|

    await sqlite_db.sql_add_command(state) #Из файла database/sqlite_db врубаем функцию sql_add_command

    await state.finish()  #Полностью очищается этот словарь и бот выходит из машины состояний, так что все свои дела со словорем должны быть закончены до этого выражения

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del ')) #Проходимся по событиям, если начинается с del то
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', '')) #
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} delete.', show_alert=True)

#@dp.message_handler(commands='Удалить') #Реакция на команду
async def delete_item(message: types.Message):
    if message.from_user.id == ID_admin: #Проверка на модератора
        read = await sqlite_db.sql_read2() #Читаем из модуля sqlite_db
        for ret in read: #Проходимся по списку
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Description: {ret[2]}\n Price: {ret[-1]}') #Отправляем фото
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().\
                    add(InlineKeyboardButton(f'Delete {ret[1]}', callback_data=f'del {ret[1]}'))) #К фото добавляем 1 инлайн кнопку и в итоге будем возвращать 'del название'

def register_handlers_admin(dp : Dispatcher):  # в main надо импортировать
    dp.register_message_handler(cm_start, commands=['Upload'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands=['Cancel'])
    dp.register_message_handler(cancel_handler, Text(equals='Cancel', ignore_case=True), state='*')  #Не забыть Text импортировать из aiogram.dispatcher.filters
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)   #('name def', Аргументы из декоратора)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['Moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands = ['Delete'])