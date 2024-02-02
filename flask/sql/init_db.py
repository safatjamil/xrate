import sys
import sqlite3
import yaml

connection = sqlite3.connect("xrate.db")

# Create table
try:
    with open("create_table.sql") as f:
        connection.executescript(f.read())
except:
    sys.exit()

# Create users
cur = connection.cursor()
users = {}
try:
    with open("../../users.yaml", "r") as f:
        users = yaml.safe_load(f)
    for user in users.keys():
        cur.execute(f"INSERT INTO users (username, password) \
                      VALUES ({user}, {users[user]['password']})"
                   )
except:
    print("Couldn't create users")
    
# Create details
cur.execute("INSERT INTO details (last_updated, timezone) \
             VALUES ('None', 'None')"
           )

connection.commit()
connection.close()
