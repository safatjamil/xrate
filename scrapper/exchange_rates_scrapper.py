import requests
from bs4 import BeautifulSoup
import resources


class ExchangeRatesOrg:
    
    def __init__(self):
        self.url = "https://www.exchange-rates.org/current-rates/usd"
        self.regions = [
            "cross-rates-body cross-rates-from-NA", 
            "cross-rates-body cross-rates-from-SA",
            "cross-rates-body cross-rates-from-EU", 
            "cross-rates-body cross-rates-from-AF",
            "cross-rates-body cross-rates-from-ME", 
            "cross-rates-body cross-rates-from-AS",
            "cross-rates-body cross-rates-from-OC"
            ]
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
        for i in range(len(self.regions)):
            div_ = soup.find("div", {"class": self.regions[i]})
            sections = div_.find_all("div", {"class": "row"})
            for section in sections:
                curr_section = section.find(class_="crr")
                if not curr_section:
                    continue
                rate_section = curr_section.find(class_="c")
                if not rate_section:
                    continue
                rate = rate_section.a
                currency = rate_section.find(class_="rn")
                if not rate or not currency:
                    continue
                rate = rate.text.replace("\r", "").replace("\n", "")
                currency = currency.text.replace("\r", "").replace("\n", "").split("/")
                if (currency[1].strip()) not in self.currencies:
                    continue
                self.exchange_rates[currency[1].strip()] = rate
        response_message["code"] = self.response_codes["ok"]
        response_message["message"] = "Parsed data successfully"
        response_message["data"] = self.exchange_rates
        return response_message

rates = ExchangeRatesOrg()
exchange_rates = rates.parse_exchange_rates()

