import sys
import sqlite3
import yaml
from datetime import datetime

now_ = datetime.now()
date_ = now_.date()
time_ = now_.strftime("%H:%M")
timezone_ = now_.astimezone().tzinfo.tzname(now_.astimezone())

connection = sqlite3.connect("xrate.db")
cur = connection.cursor()

# Create table
try:
    with open("tables.sql") as f:
        connection.executescript(f.read())
except:
    sys.exit()

# Create users
try:
    with open("../../users.yaml", "r") as f:
        users = yaml.safe_load(f)
    if not users:
        print("No users found")
        sys.exit()
    for user in users.keys():
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", \
                     (user, users[user]['password']))
except:
    print("Couldn't create users. Check the users.yaml file")
    sys.exit()
    
# Create details
cur.execute("INSERT INTO details (date_, time_, timezone) VALUES (?, ?, ?)", \     
            (date, time, timezone)) 

connection.commit()
connection.close()
