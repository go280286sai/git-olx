import sqlite3 
#-----------------------------------------------------------------------------------------------------------------------------
con = sqlite3.connect('database.db')
cur = con.cursor()
#-----------------------------------------------------------------------------------------------------------------------------
con.execute("""CREATE TABLE IF NOT EXISTS settings(
settingsID INTEGER PRIMARY KEY AUTOINCREMENT,
komnati text,
etajnost text,
ref text);""")
con.commit
print("1 - просмотр настроек, 2 - изменить настройки, 0 - выход")
n=int(input("Введите циифру "))

while n!=0:
    
#-----------------------------------------------------------------------------------------------------------------------------
    if n==1:   
        sqlite_select_query = """SELECT * from settings"""
        t=con.execute(sqlite_select_query)
        path=t.fetchone()
        con.commit()
        print("Количество комнат:",path[1])
        print("Этажность:",path[2])
        print("ref:",path[3])
#-----------------------------------------------------------------------------------------------------------------------------
    if n==2:
        komnati=str(input('Введите количество комнат '))
        etajnost=str(input('Введите этажность '))
        ref=str(input('Введите ссылку '))
        if (komnati!='' and komnati.isdigit()) and  etajnost!='' and etajnost.isdigit():
            con.execute("UPDATE settings SET komnati=?",komnati)
            con.execute("UPDATE settings SET etajnost=?", etajnost)
            con.execute("UPDATE settings SET ref=?", ref)
            con.commit()
            print('Данные успешно обновлены!')
        else:
            print("Не корректный ввод данных, попробуйте еще!")
            
#-----------------------------------------------------------------------------------------------------------------------------
    print("1 - просмотр настроек, 2 - изменить настройки, 0 - выход")
    n=int(input("Введите циифру "))