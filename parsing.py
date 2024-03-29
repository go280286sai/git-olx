import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import sqlite3 
import os
#-----------------------------------------------------------------------------------------------------------------------------
con = sqlite3.connect('database.db')
cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------------------
today_day=datetime.today().strftime('%Y-%m-%d')
file_name='parsing_olx_{}.csv'
FILE=file_name.format(today_day)
#-----------------------------------------------------------------------------------------------------------------------------
URL = 'https://www.olx.ua'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r
#-----------------------------------------------------------------------------------------------------------------------------
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='item fleft')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1
#-----------------------------------------------------------------------------------------------------------------------------
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='offer-wrapper')
    mass = []
    for item in items:
        mass.append({
            'title': item.find('strong').get_text(strip=True),
            'link': item.find('a').get('href'),
            'price': item.find('strong').find_next('strong').get_text(),
            'location' : item.find('p').find_next('p', class_='lheight16').get_text().split()[1]
        })
    return mass
#-----------------------------------------------------------------------------------------------------------------------------
def save_file(items, path):
    with open(path, 'w', newline='',  encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['title', 'ref', 'location', 'price'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['location'] ,item['price']])
#-----------------------------------------------------------------------------------------------------------------------------
def parse():
    print('1. Ввести URL вручную')
    print('2. Ввести URL из настроек')
    n = int(input('Введите цифру '))
    if n == 1:
        URL = input('Insert URL: ')
    elif n == 2:
        sqlite_select_query = """SELECT ref from settings"""
        cur.execute(sqlite_select_query)
        records = cur.fetchone()
        mas = []
        mas.append(records[0])
        URL =  mas[0]  
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        mass = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            mass.extend(get_content(html.text))
        save_file(mass, 'data/'+FILE)
        print(f'Get {len(mass)} count')
    else:
        print('Error')

#-----------------------------------------------------------------------------------------------------------------------------
con.execute("""CREATE TABLE IF NOT EXISTS create_parse(
create_parse INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
path TEXT);""")

#-----------------------------------------------------------------------------------------------------------------------------
path='data/'+FILE
nmas=[FILE, path]
con.execute("""INSERT INTO create_parse(name, path) VALUES (?, ?);""", nmas)
con.commit()
