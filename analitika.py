import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sqlite3
#-----------------------------------------------------------------------------------------------------------------------------
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
kurs=pd.DataFrame({'Kurs_$':[USD_buy, USD_sell]})
kurs.to_csv('analitika.csv')
print(kurs)
#-----------------------------------------------------------------------------------------------------------------------------
con.execute("""CREATE TABLE IF NOT EXISTS kurs(
create_kurs INTEGER PRIMARY KEY AUTOINCREMENT,
data_k DATE,
USD_buy REAL,
USD_sell REAL);""")
con.commit()
#-----------------------------------------------------------------------------------------------------------------------------
today_day=datetime.today().strftime('%Y-%m-%d')
sqlite_select_query = """SELECT data_k from kurs"""
cur.execute(sqlite_select_query)
records = cur.fetchall()
Kmas=[today_day, USD_buy, USD_sell]
con.execute("""INSERT INTO kurs(data_k, USD_buy, USD_sell) VALUES (?, ?, ?);""", Kmas)
con.commit()
#-----------------------------------------------------------------------------------------------------------------------------
data=pd.read_csv('full_parser.csv')
data_type=data.groupby('type_b', as_index=False).count()[['type_b', 'title']]
data_type.to_csv('analitika.csv', mode='a')
print(data_type)
#-----------------------------------------------------------------------------------------------------------------------------
data_local=data.groupby('local', as_index=False).count()[['local', 'title']]
data_local.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
data_local_mean=data.groupby('local', as_index=False).agg({'price':'mean'})
data_local_mean.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_local_mean)
print(data_local)
#-----------------------------------------------------------------------------------------------------------------------------
data_local_max=data_local_mean.max()
data_local_max.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_local_max)
#-----------------------------------------------------------------------------------------------------------------------------
data_local_min=data_local_mean.min()
data_local_min.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_local_min)
#-----------------------------------------------------------------------------------------------------------------------------
data_etajnost=data.groupby('etajnost', as_index=False).count()[['etajnost', 'title']]
data_etajnost.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_etajnost)
#-----------------------------------------------------------------------------------------------------------------------------
data_komnati=data.groupby('komnati', as_index=False).count()[['komnati','title']]
data_komnati.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_komnati)
#-----------------------------------------------------------------------------------------------------------------------------
data_full=data.groupby(['etajnost', 'etaj'],  as_index=False).agg({'komnati':'count'})
data_full.to_csv('analitika.csv', mode='a')
#-----------------------------------------------------------------------------------------------------------------------------
print(data_full)
print(data.columns)