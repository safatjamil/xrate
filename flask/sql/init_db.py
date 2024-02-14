import sys
import sqlite3
import yaml
from datetime import datetime

sys.path.append("../..")
from resources.cryptograp import Encrypt
from resources.encode_decode import EncodeDecode
now_ = datetime.now()
datetime_ = {"date": now_.date(),
             "time": now_.strftime("%H:%M"),
             "timezone": now_.astimezone().tzinfo.tzname(now_.astimezone())
            }

class InitDb:
    
    def __init__(self):
        self.__connection = sqlite3.connect("/xrate/flask/sql/xrate.db", 
                                            check_same_thread=False)
        self.__cur = self.__connection.cursor()
    def create_tables(self):
        response = {"status": "", "message": ""}
        try:
            with open("/xrate/flask/sql/tables.sql") as f:
                self.__connection.executescript(f.read())
        except:
            response["status"] = False
            response["message"] = "Couldn't create tables"
            return response
        response["status"] = True
        response["message"] = "Successfully created the tables"
        return response

    def create_users(self):
        response = {"status": "", "message": ""}
        try:
            with open("../../resources/users.yaml", "r") as f:
                users = yaml.safe_load(f)
            if not users:
                response["status"] = False
                response["message"] = "No users found"
                return response
            for user in users.keys():
                password = Encrypt.hash_password(
                               EncodeDecode.decode(users[user]['password']))
                self.__cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",\
                (user, password))
        except:
            response["status"] = False
            response["message"] = "Couldn't create users. Check the users.yaml file"
            return response
        response["status"] = True
        response["message"] = "Created users successfully"
        return response
    
    def create_details(self): 
        self.__cur.execute("INSERT INTO details (date, time, timezone) VALUES (?, ?, ?)",\
        (datetime_["date"], datetime_["time"], datetime_["timezone"])) 
    
    def commit(self):
        self.__connection.commit()
        self.__connection.close()


init_db = InitDb()
init_db.create_tables()
init_db.create_users()
init_db.create_details()
init_db.commit()