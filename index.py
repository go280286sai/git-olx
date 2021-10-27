#!/bin/python3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import settings
import parsing
import view
m = True
while m == True:
    print('Добрый день, выберете действие:')
    print('1. Выполнить парсинг сайта')
    print('2. Выполнить детальный парсинг сайта')
    print('3. Изменить настройки')
    print('0. Выход из программы')
    n = int(input('Введите номер: '))
    if n == 0:
        m = False
    if n == 1:
        parsing.parse()
    if n == 2:
        view.get_full()    
    if n == 3:
        settings.setf()
