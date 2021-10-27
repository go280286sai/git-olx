import requests
from bs4 import BeautifulSoup
import sqlite3 
import pandas as pd
from datetime import datetime
#-----------------------------------------------------------------------------------------------------------------------------
#today_day=datetime.today().strftime('%Y-%m-%d')
#file_name='parsing_olx_{}.xlsx'
#FILE=file_name.format(today_day)
#-----------------------------------------------------------------------------------------------------------------------------
con = sqlite3.connect('database.db')
cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------------------
def my_price(price):
    price=str(price)
    total=''
    for i in range(len(price)):
        if price[i]!=' ':
            total+=price[i]
    total=total[:-1]
    return float(total)
def get_ref(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    return items

#-----------------------------------------------------------------------------------------------------------------------------    
def scan_full_type_b(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    mass=[]
    for item in items:
        mass.append(item.get_text())
    for item in mass:
        if 'Бизнес' in item:
            type_b='Бизнес'
            break
        if 'Частное лицо' in item:
            type_b='Владелец'
            break
    return type_b

#-----------------------------------------------------------------------------------------------------------------------------
def scan_full_etajnost(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    mass=[]
    for item in items:
        mass.append(item.get_text())
    for item in mass:
        if 'Этажность:' in item:
            etajnost=str(item.split()[-1])
            break
    return etajnost
#-----------------------------------------------------------------------------------------------------------------------------
def scan_full_etaj(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    mass=[]
    for item in items:
        mass.append(item.get_text())
    for item in mass:
        if 'Этаж:' in item:
            etaj=str(item.split()[-1])
            break
    return etaj
#-----------------------------------------------------------------------------------------------------------------------------  
def scan_full_komnati(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    mass=[]
    for item in items:
        mass.append(item.get_text())
    for item in mass:
        if 'Количество комнат:' in item:
            komnati=item.split()
            komnati=str(komnati[2])
            break
    if komnati!=0 and komnati!='' and komnati!=' ':
        return komnati
    else:
        return 0
#-----------------------------------------------------------------------------------------------------------------------------    
def scan_full_opis(ref):
    URL=str(ref)
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
    r=requests.get(URL, params=None, headers=HEADERS)
    html_doc=r.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    mass=[]
    for item in items:
        mass.append(item.get_text())
    opis=soup.find('div', class_='css-g5mtbi-Text').get_text()
    return opis
#-----------------------------------------------------------------------------------------------------------------------------
sqlite_select_query = """SELECT path from create_parse ORDER BY path DESC LIMIT 1"""
t=con.execute(sqlite_select_query)
path=t.fetchone()
con.commit()
path=str(path[0])

#-----------------------------------------------------------------------------------------------------------------------------
def get_full():
    data=pd.read_csv(path, sep=';')
    data=data.head(300)
    data['price']=data.price.apply(my_price)
    data['type_b']=data.ref.apply(scan_full_type_b)
    data['etajnost']=data.ref.apply(scan_full_etajnost)
    data['etaj']=data.ref.apply(scan_full_etaj)
    data['komnati']=data.ref.apply(scan_full_komnati)
    data['opis']=data.ref.apply(scan_full_opis)
    data.to_csv('full_parser.csv', sep=';')
    print('ok')
