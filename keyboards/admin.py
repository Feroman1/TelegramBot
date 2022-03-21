from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#Кнопки админа
button_load = KeyboardButton('/Upload')
button_delete = KeyboardButton('/Delete')
button_cancel = KeyboardButton('/Cancel')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard = True).add(button_load).add(button_delete).add(button_cancel)