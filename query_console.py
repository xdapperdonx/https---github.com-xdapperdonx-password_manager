import sqlite3

conn = sqlite3.connect("password.db")
c = conn.cursor()

sql_command = input("Enter the SQL command: ")
c.execute(sql_command)
print(c.fetchall())

conn.commit()
conn.close()
