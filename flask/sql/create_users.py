import sqlite3
import yaml

connection = sqlite3.connect("xrate.db")
cur = connection.cursor()
users = {}
try:
    with open("../../users.yaml", "r") as f:
        users = yaml.safe_load(f)
    for user in users.keys():
        cur.execute(f"INSERT INTO users (username, password) 
                      VALUES ({user}, {users[user]['password']})"
                   )
connection.commit()
connection.close()
