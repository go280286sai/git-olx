from os import path
import sqlite3 

con = sqlite3.connect('database.db')
cur = con.cursor()
con.execute("""CREATE TABLE IF NOT EXISTS settings(
settingsID INTEGER PRIMARY KEY AUTOINCREMENT,
ref text);""")
con.commit


def fetch():
    sqlite_select_query = """SELECT * from settings"""
    t=con.execute(sqlite_select_query)
    perem1=t.fetchone()
    con.commit()
    return perem1

def setf():
    k = True
    while k==True:
        print("1 - просмотр настроек")
        print("2 - изменить настройки")
        print("0 - выход")
        n=int(input("Введите циифру "))
        if n==1:   
            path = fetch()
            if path == None:
                print("Настройки пусты")
            else:
                print("ref:",path[1])
        elif n==2:
            ref_1=str(input('Введите ссылку '))
            path = fetch()
            if path == None:
                spisok = [ref_1]
                con.execute("""INSERT INTO settings (ref) VALUES (?);""", spisok)
                con.commit()
                print('Данные успешно добавлены!') 
            else: 
                con.execute("UPDATE settings SET ref=? WHERE settingsID=1", [ref_1])
                con.commit()
                print('Данные успешно обновлены!') 
        elif n == 0:
            k = False