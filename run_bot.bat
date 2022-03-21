@echo off

call %~dp0venv\Scripts\activate #Путь откуда открывать

cd %~dp0 #Переход в папку командной строки

set TOKEN= 'Your token'

python main.py #Что запустить

pause
