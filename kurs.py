#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
#-----------------------------------------------------------------------------------------------------------------------
con = sqlite3.connect('database.db')
cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------------------
URL='https://privatbank.ua/ru'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
#-----------------------------------------------------------------------------------------------------------------------------
r=requests.get(URL, params=None, headers=HEADERS)
html_doc=r.text
soup = BeautifulSoup(html_doc, 'html.parser')
USD_buy = soup.find('td', id='USD_buy').get_text()
USD_sell=soup.find('td', id='USD_sell').get_text()
USD_buy =float(USD_buy)
USD_sell=float(USD_sell)
#-----------------------------------------------------------------------------------------------------------------------------
con.execute("""CREATE TABLE IF NOT EXISTS kurs(
create_kurs INTEGER PRIMARY KEY AUTOINCREMENT,
data_k TEXT,
USD_buy REAL,
USD_sell REAL);""")
con.commit()
#-----------------------------------------------------------------------------------------------------------------------------
today_day=datetime.today().strftime('%Y-%m-%d')
sqlite_select_query = """SELECT data_k from kurs"""
cur.execute(sqlite_select_query)
records = cur.fetchall()
mas=[]
k=0
while k!=len(records):
    mas.append(records[k][0])
    k+=1
if today_day in mas:
    print("На текущую дату курс выставлен")
else:       
    Kmas=[today_day, USD_buy, USD_sell]
    con.execute("""INSERT INTO kurs(data_k, USD_buy, USD_sell) VALUES (?, ?, ?);""", Kmas)
    con.commit()
print('Курс продать:', USD_buy)
print('Курс купить:', USD_sell)
