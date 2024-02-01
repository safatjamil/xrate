import sys
from flask import Flask, jsonify, request
sys.path.append("..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg

app = Flask(__name__)
calculator_net = CalculatorNet()
exchange_rates_org = ExchangeRatesOrg()

@app.route("/api/test/", methods = ["GET"])
def test_status():
    response = {"status": "OK"}
    return jsonify(response), 200

@app.route("/api/rates/update/", methods = ["GET"])
def update_rates():
    response = {}
    data = calculator_net.parse_exchange_rates()
    if data["code"] == 200:
        response["data"] = data["data"]
        response["message"] = f"{len(data['data'].keys())} currencies updated"
        return jsonify(response), 200
    else:
        data = exchange_rates_org.parse_exchange_rates()
        if data["code"] == 200:
            response["data"] = data["data"]
            response["message"] = f"{len(data['data'].keys())} currencies updated"
            return jsonify(response), 200
        else:
            response["message"] = "Couldn't update data"
            return jsonify(response), response["code"]
