import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import kurs

m = True
while m == True:
    print('Добрый день, выберете действие:')
    print('1. Выполнить парсинг сайта')
    print('2. Выполнить парсинг сайта на основе общего')
    print('3. Вывести аналитические данные')
    print('4. Загрузить курсы валют')
    print('5. Изменить настройки')
    print('0. Выход из программы')
    n = int(input('Введите номер: '))
    if n == 0:
        m = False
    if n == 4:
        kurs.kurs()
