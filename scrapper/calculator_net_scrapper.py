import re
import requests
from bs4 import BeautifulSoup
import resources


class CalculatorNet:

    def __init__(self):
        self.url = "https://www.calculator.net/currency-calculator.html"
        self.currencies = resources.ScrapppingResources.currencies
        self.response_codes = resources.Response.codes
        self.exchange_rates = {}
    
    def parse_exchange_rates(self):
        response_message = {"code": "", "error": "", "message": "", "data": {}}
        request = requests.get(self.url, timeout=20)
        if request.status_code != 200:
            response_message["code"] = request.status_code
            response_message["error"] = "Couldn't initiate a valid response"
            return response_message
        soup = BeautifulSoup(request.content, "html.parser")
        script = soup.find_all("script")[2].text
        if not script:
            response_message["code"] = self.response_codes["upgrade"]
            response_message["error"] = "Couldn't parse data"
            return response_message
        pattern = "var listsArrayData .*]];"
        raw_data = re.findall(pattern, script, re.S)
        if not raw_data or len(raw_data[0]) < 30:
            response_message["code"] = self.response_codes["upgrade"]
            response_message["error"] = "Couldn't parse data"
            return response_message
        rates = eval(raw_data[0][21:-1])
        for i in range(len(rates)):
            if rates[i][0] in self.currencies:
                self.exchange_rates[rates[i][0]] = rates[i][1]
        response_message["code"] = self.response_codes["ok"]
        response_message["message"] = "Parsed data successfully"
        response_message["data"] = self.exchange_rates
        return response_message

calculatornet = CalculatorNet()
rates = calculatornet.parse_exchange_rates()
print(rates)
print(len(rates["data"].keys()))

