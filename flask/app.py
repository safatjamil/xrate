import sys
from flask import Flask, jsonify, request
sys.path.append("..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources.currencies import Currencies
from resources.response import Response
from auth.authenticate_user import AuthUser
app = Flask(__name__)
calculator_net = CalculatorNet()
exchange_rates_org = ExchangeRatesOrg()

@app.route("/api/test/", methods = ["GET"])
def test_status():
    response = {"status": "OK"}
    return jsonify(response), 200


@app.route("/api/<from_>-<to>/", methods = ["GET"])
def convert_currency(from_, to):
    response = {}
    try:
        data = request.get_json()
    except:
        response = {"message": "Invalid request"}
        return jsonify(response), 400
    if from_ not in Currencies.currencies or to not in Currencies.currencies:
        response = {"message": "Invalid currency"}
        return jsonify(response), 400
    response = {"message": "ok"}
    return jsonify(response), 200


@app.route("/api/rates/update/", methods = ["GET"])
def update_rates():
    response = {}
    try:
        data = request.get_json()
    except:
        response = {"status": "not ok"}
        return jsonify(response), 403



    if data["code"] == 200:
        response["data"] = data["data"]
        update_rates.update(data["data"])
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


@app.route("/api/<currency>/last-updated/", methods = ["GET"])
def currency_last_updated(currency):
    currency = currency.upper()
    response = {}
    if len(currency) != 3:
        response["message"] = "This is not a valid currency"
        response["code"] = Response.codes["bad_format"]
        return jsonify(response), response["code"]
    if currency.upper() not in Currencies.currencies:
        response["message"] = "We do not support this currency right now. Please send an email to safaetxamil@yahoo.com for support. Thanks"
        response["code"] = Response.codes["not_found"]
        return jsonify(response), response["code"]