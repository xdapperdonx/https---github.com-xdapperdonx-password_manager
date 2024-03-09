import sqlite3

conn = sqlite3.connect('password.db')

c = conn.cursor()

c.execute("CREATE TABLE passwords ( website text, username text, password text, tag text, nonce text)")

conn.commit()

conn.close()
