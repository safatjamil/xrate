import sys
from flask import Flask, jsonify, request
sys.path.append("..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources.currencies import Currencies
from resources.response import Response
from auth.authenticate_user import AuthUser
from sql.query import Query

app = Flask(__name__)
calculator_net = CalculatorNet()
exchange_rates_org = ExchangeRatesOrg()
response_codes = Response.codes
query = Query()
auth_user = AuthUser()

@app.route("/api/test/", methods = ["GET"])
def test_status():
    response = {"status": "OK"}
    return jsonify(response), 200

@app.route("/api/<from_>-<to>/", methods = ["GET"])
def convert_currency(from_, to):
    response = {"message": "", "data": ""}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide your username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth["status"]:
        response["message"] = auth["message"]
        return jsonify(response), response_codes["auth_error"]
    if from_ not in Currencies.currencies or to not in Currencies.currencies:
        response["message"] = "Invalid currency"
        return jsonify(response), response_codes["bad_request"]
    from_curr_value = query.currency_value(from_)
    print(from_curr_value)
    response = {"message": "ok"}
    return jsonify(response), response_codes["ok"]


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