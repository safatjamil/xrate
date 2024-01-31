import sqlite3

connection = sqlite3.connect("xrate.db")

with open("create_table.sql") as f:
    connection.executescript(f.read())