from aiogram import types,Dispatcher
from create_bot import dp

import string, json

#@dp.message_handler()
async def command_no_mat(message : types.Message):
    if {i.lower().translate(str.maketrans("", "", string.punctuation)) for i in message.text.split(' ')}.intersection(set(json.load(open('cenz.json')))) != set(): #Если в сообщении есть мат, то оно не равняется пустому и следоватльно проходит дальше
        await message.reply("Swearing is prohibited!")
        await message.delete()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(command_no_mat) #Функция анти мат