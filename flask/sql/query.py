import sys
import sqlite3
from datetime import datetime

sys.path.append("../..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources import currencies


class Query:

    def __init__(self):
        self.__connection = sqlite3.connect("/xrate/flask/sql/xrate.db")
    
    def currency_value(self, currency):
        response = {"status": False, "message": "", "data": ""}
        cur = self.__connection.cursor()
        try:
            cur.execute("SELECT * FROM rates WHERE currency=?", (currency))
            row = cur.fetchone()
            if not row:
                response["status"] = False
                response["message"] = "Currency not found"
                return response
            print(row)
            response["status"] = True
            response["message"] = "Success"
            response["data"] = row[0][2]
            return response
        except:
            response["status"] = False
            response["message"] = "Something went wrong"
            return response
