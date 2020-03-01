import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


createtable = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(createtable)

user = (1, 'Chaitu','mypass1')
insert_query = "insert into users values(?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (2, 'Divya', 'mypass2'),
    (3, 'Sweety', 'mypass3')
]

cursor.executemany(insert_query, users)

select_query = "select * from users"

for i in cursor.execute(select_query):
    print(i)
    
connection.commit()
connection.close()
