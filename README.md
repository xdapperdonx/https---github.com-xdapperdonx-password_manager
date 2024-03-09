# Password Manager

Simple python script that stores passwords in your local machine.

The following libraries are used:
1. sqlite3
2. Cryptodome 

Scripts Explained:
1. aes.py: main python script that manages the data
2. init_db.py: creates sqlite3 database
3. migrate.py: optional script, this was used to migrate data from a textfile to database
4. query_console.py: script used to access database directly 
