import sys
import sqlite3
import bcrypt
sys.path.append("../..")

class AuthUser:
    connection = sqlite3.connect("/xrate/flask/sql/xrate.db")
    def auth(username, password):
        response = {"status": False, "message": ""}
        cur = self.__connection.cursor()
        try:
            cur.execute("SELECT * FROM rates WHERE username=?", (username))
            row = cur.fetchall()
            if row == 0:
                response["status"] = False
                response["message"] = "User not found"
                return response
            user = row[0]
            if bcrypt.checkpw(password.encode("utf-8"), row[1]):
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


