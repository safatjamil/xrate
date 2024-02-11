import sys
import sqlite3
from datetime import datetime

sys.path.append("../..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources import currencies


class Query:

    def __init__(self):
        self.__connection = sqlite3.connect("/xrate/flask/sql/xrate.db",
                                            check_same_thread=False)
    
    def currency_details(self, currency):
        response = {"status": False, "message": "", "data": {}}
        cur = self.__connection.cursor()
        try:
            cur.execute("SELECT * FROM rates WHERE currency=?", (currency,))
            row = cur.fetchone()
            if not row:
                response["status"] = False
                response["message"] = "Currency not found"
                return response
            response["status"] = True
            response["message"] = "Success"
            response["data"]["rate"] = row[2]
            response["data"]["date"] = row[3]
            response["data"]["time"] = row[4]
            response["data"]["timezone"] = row[5]
            return response
        except:
            response["status"] = False
            response["message"] = "Something went wrong"
            return response

