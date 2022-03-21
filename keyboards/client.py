from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#Создаем кнопки
b2 = KeyboardButton('/WorkingHours')
b3 = KeyboardButton('/Address')
b4 = KeyboardButton('/Assortment')


kb_client = ReplyKeyboardMarkup(resize_keyboard=True)  #ReplyKeyboardMarkup - Замещение клавы на нашу #resize.... - Размер кнопок
kb_client.add(b2).add(b3).insert(b4)   #Добавляем кнопки в клаве (3 типа расположения)
