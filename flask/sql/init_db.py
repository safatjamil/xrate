import sys
import sqlite3
import yaml
from datetime import datetime

sys.path.append("../..")
from resources.cryptograp import Encrypt
from resources.encode_decode import EncodeDecode
now_ = datetime.now()
date_ = now_.date()
time_ = now_.strftime("%H:%M")
timezone_ = now_.astimezone().tzinfo.tzname(now_.astimezone())

connection = sqlite3.connect("xrate.db")
cur = connection.cursor()

class InitDb:
    def create_tables():
        response = {"status": "", "message": ""}
        try:
            with open("tables.sql") as f:
                connection.executescript(f.read())
        except:
            response["status"] = False
            response["message"] = "Couldn't create tables"
            return response
        response["status"] = True
        response["message"] = "Successfully created the tables"
        return response

    def create_users():
        response = {"status": "", "message": ""}
        try:
            with open("../../users.yaml", "r") as f:
                users = yaml.safe_load(f)
            if not users:
                response["status"] = False
                response["message"] = "No users found"
                return response
            for user in users.keys():
                password = Encrypt.hash_password(
                               EncodeDecode.decode(users[user]['password'])))
                cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", \
                            (user, password))
        except:
            response["status"] = False
            response["message"] = "Couldn't create users. Check the users.yaml file"
            return response
        response["status"] = True
        response["message"] = "Created users successfully"
        return response
    
    def create_details():
        
cur.execute("INSERT INTO details (date_, time_, timezone) VALUES (?, ?, ?)", \     
            (date, time, timezone)) 

connection.commit()
connection.close()
