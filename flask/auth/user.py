import sys
import sqlite3
import bcrypt
sys.path.append("../..")

class AuthUser:

    def __init__(self):
        self.__connection = sqlite3.connect("/xrate/flask/sql/xrate.db", check_same_thread=False)

    def auth(self, username, password):
        response = {"status": False, "message": ""}
        cur = self.__connection.cursor()
        try:
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            row = cur.fetchall()
            if len(row) == 0:
                response["status"] = False
                response["message"] = "User not found"
                return response
            user = row[0]
            if bcrypt.checkpw(password.encode("utf-8"), user[2]):
                response["status"] = True
                response["message"] = "User not found"
                return response
            response["status"] = False
            response["message"] = "Wrong credentials"
            return response
        except:
            response["status"] = False
            response["message"] = "Something went wrong"
            return response


