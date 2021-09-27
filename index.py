import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
import kurs
import settings

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
        k = True


        while k == True:
            print('1. Загрузить новые курсы валют')
            print('2. Просмотреть курсы валют')
            print('0. Выйти в предыдущее меню') 
            ks = int(input('Введите номер: '))
            if ks == 1: 
                kurs.kurs()
            elif ks == 2:
                kurs.tab_kurs()
            elif ks == 0:
                k = False
            else:
                print("Вы не правильно ввели цифру, попробуйте еще")
    if n == 5:
        settings.setf()
