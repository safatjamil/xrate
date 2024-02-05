import sys
import sqlite3
import yaml
from datetime import datetime

sys.path.append("../..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources import currencies, response


now_ = datetime.now()
date_ = now_.date()
time_ = now_.strftime("%H:%M")
timezone_ = now_.astimezone().tzinfo.tzname(now_.astimezone())


class UpdateRates():
    
    def __init__(self):
        self.currencies = currencies.Currencies.currencies
        self.now_ = datetime.now()
        self.time_attr = {"date": self.now_.date(), 
                          "time": self.now_.strftime("%H:%M"),
                          "timezone": self.now_.astimezone().\
                                      tzinfo.tzname(now_.astimezone())
                         }                
        self.__connection = sqlite3.connect("/xrate/flask/sql/xrate.db")
    
    def update(self, rates):
        cur = self.__connection.cursor()
        for rate in rates.keys():
            if rate not in self.currencies:
                continue
            cur.execute("REPLACE INTO rates (currency, rate, date, time, timezone) \
                         VALUES(?, ?, ?, ?, ?)",\
                         (rate, rates[rate], self.time_attr["date"], self.time_attr["time"],\
                          self.time_attr["timezone"]))

        cur.execute("REPLACE INTO details (date, time, timezone) VALUES (?, ?, ?)", \
                    (self.time_attr["date"], self.time_attr["time"],\
                     self.time_attr["timezone"]))
        self.__connection.commit()
        self.__connection.close()

          



            
            


