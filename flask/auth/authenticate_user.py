import sys
import sqlite3
sys.path.append("../..")

class AuthUser:
    connection = sqlite3.connect("/xrate/flask/sql/xrate.db")
    def auth(username, password):
        response = {"status": False, "message": ""}
        cur = self.__connection.cursor()


