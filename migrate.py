import sqlite3

conn = sqlite3.connect("password.db")
c = conn.cursor()

filepath = #insert path to text file

with open(filepath, "r") as file:
    
    for line in file:
        
        line_data = line.split(', ')
        
        website = line_data[0]
        username = line_data[1]
        encrypted_password = line_data[2]
        tag = line_data[3]
        nonce = line_data[4]

        c.execute(f"INSERT INTO passwords VALUES('{website}', '{username}', '{encrypted_password}', '{tag}', '{nonce}')")

        conn.commit()
conn.close() 
