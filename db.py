import sqlite3


# connexion to the database
conn = sqlite3.connect('data/cygnet.db')
Database = conn.cursor()
