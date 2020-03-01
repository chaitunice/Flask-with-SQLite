import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

create_query = "CREATE Table if not exists users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_query)

create_items = "create Table if not exists items (name text, price real)"
cursor.execute(create_items)

cursor.execute("Insert into items values('Laptop',1299)")

conn.commit()
conn.close()

