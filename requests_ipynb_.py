
import requests
from bs4 import BeautifulSoup
URL=str(input())
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
r=requests.get(URL, params=None, headers=HEADERS)
html_doc=r.text
soup = BeautifulSoup(html_doc, 'html.parser')
items = soup.find_all('p', class_='css-xl6fe0-Text eu5v0x0')
for item in items:
    print(item.get_text())
opis=soup.find('div', class_='css-g5mtbi-Text').get_text()
print(opis)
d=int(input())