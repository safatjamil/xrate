import sys
import sqlite3
import yaml

connection = sqlite3.connect("xrate.db")

# Create table
try:
    with open("tables.sql") as f:
        connection.executescript(f.read())
except:
    sys.exit()

# Create users
cur = connection.cursor()
try:
    with open("../../users.yaml", "r") as f:
        users = yaml.safe_load(f)
    if not users:
        print("No users found")
        sys.exit()
    for user in users.keys():
        cur.execute("INSERT INTO users (username, password_) VALUES (?, ?)", \
                     (user, users[user]['password']))
except:
    print("Couldn't create users. Check the users.yaml file")
    sys.exit()
    
# Create details
cur.execute("INSERT INTO details (last_updated, timezone) \
             VALUES ('None', 'None')"
           )

connection.commit()
connection.close()
