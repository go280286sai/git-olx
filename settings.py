from os import path
import sqlite3 

con = sqlite3.connect('database.db')
cur = con.cursor()
con.execute("""CREATE TABLE IF NOT EXISTS settings(
settingsID INTEGER PRIMARY KEY AUTOINCREMENT,
komnati text,
etajnost text,
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
                print("Количество комнат:",path[1])
                print("Этажность:",path[2])
                print("ref:",path[3])
    
        elif n==2:
            komnati_1=str(input('Введите количество комнат '))
            etajnost_1=str(input('Введите этажность '))
            ref_1=str(input('Введите ссылку '))
            path = fetch()
            if path == None:
                spisok = [komnati_1, etajnost_1, ref_1]
                con.execute("""INSERT INTO settings (komnati, etajnost, ref) VALUES (?, ?, ?);""", spisok)
                con.commit()
                print('Данные успешно добавлены!') 
            else: 
                if (komnati_1!='' and komnati_1.isdigit()) and  etajnost_1!='' and etajnost_1.isdigit():
                    con.execute("UPDATE settings SET komnati=?",komnati_1)
                    con.execute("UPDATE settings SET etajnost=?", etajnost_1)
                    con.execute("UPDATE settings SET ref=? WHERE settingsID=1", [ref_1])
                    con.commit()
                    print('Данные успешно обновлены!') 
                else:
                    print("Не корректный ввод данных, попробуйте еще!")
        elif n == 0:
            k = False
        elif n == str:
            print("Введите цифру, а не текст")

   