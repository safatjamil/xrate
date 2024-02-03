import sys
import sqlite3
import yaml
from datetime import datetime

connection = sqlite3.connect("xrate.db")

now_ = datetime.now()
date_ = now.date()
time_ = now_.strftime("%H:%M")
timezone_ = now_.astimezone().tzinfo.tzname(now_.astimezone())

class UpdateRates():

    def __init__(self, rates):
        self.rates = rates
        self.date_ = date_
        self.time_ = time_
        self.timezone_ = timezone_
        self.connection = connection
    
    def update_calculator_net(self):
        for rate in self.rates.keys():
            pass


