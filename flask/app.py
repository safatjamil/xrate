import sys
from flask import Flask, jsonify, request
sys.path.append("..")
from scrapper.calculator_net_scrapper import CalculatorNet
from scrapper.exchange_rates_scrapper import ExchangeRatesOrg
from resources.currencies import Currencies
from resources.response import Response
from auth.user import AuthUser
from sql.query import Query
from sql.update_rates import UpdateRates


app = Flask(__name__)
calculator_net = CalculatorNet()
exchange_rates_org = ExchangeRatesOrg()
response_codes = Response.codes
query = Query()
auth_user = AuthUser()
update_rates = UpdateRates()

@app.route("/api/test/", methods = ["GET"])
def test_status():
    response = {"status": "ok"}
    return jsonify(response), 200

@app.route("/api/user/auth/", methods = ["GET"])
def authenticate_user():
    response = {"status": "error", "message": "", "data": {}}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide your username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth_["status"]:
        response["message"] = auth_["message"]
        return jsonify(response), response_codes["auth_error"]
    response["status"] = "ok"
    response["message"] = "User authentication successful"
    return jsonify(response), response_codes["ok"]
    

@app.route("/api/rates/update/", methods = ["POST"])
def update_curr_rates():
    response = {"status": "error", "message": "", "data": {}}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide you r username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth_["status"]:
        response["message"] = auth_["message"]
        return jsonify(response), response_codes["auth_error"]
    data = calculator_net.parse_exchange_rates()
    if data["code"] == 200:
        update_rates.update(data["data"])
        response["status"] = "ok"
        response["data"] = data["data"]
        response["message"] = f"{len(data['data'].keys())} currencies updated"
        return jsonify(response), 200
    else:
        data = exchange_rates_org.parse_exchange_rates()
        if data["code"] == 200:
            update_rates.update(data["data"])
            response["status"] = "ok"
            response["message"] = f"{len(data['data'].keys())} currencies updated"
            response["data"] = data["data"]
            return jsonify(response), 200
        else:
            response["message"] = "Couldn't update data"
            return jsonify(response), response["code"]


@app.route("/api/convert/<from_>-<to_>/", methods = ["GET"])
def convert_currency(from_, to_):
    from_ = from_.upper()
    to_ = to_.upper()
    response = {"status": "error", "message": "", "data": {}}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide you r username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth_["status"]:
        response["message"] = auth_["message"]
        return jsonify(response), response_codes["auth_error"]
    if from_ not in Currencies.currencies or to_ not in Currencies.currencies:
        response["message"] = "Invalid currency"
        return jsonify(response), response_codes["bad_request"]
    from_curr_value = query.currency_details(from_)
    if not from_curr_value["status"]:
        response["message"] = from_curr_value["message"]
        return jsonify(response), response_codes["unavailable"]
    to_curr_value = query.currency_details(to_)
    if not to_curr_value["status"]:
        response["message"] = to_curr_value["message"]
        return jsonify(response), response_codes["unavailable"]
    
    response["status"] = "ok"
    response["message"] = "Successful"
    response["data"]["conv_rate"] = (1/from_curr_value["data"]["rate"])*\
                                    to_curr_value["data"]["rate"]
    return jsonify(response), response_codes["ok"]

@app.route("/api/convert-all/<currency>/", methods = ["GET"])
def convert_to_all(currency):
    currency = currency.upper()
    response = {"status": "error", "message": "", "data": {}}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide you r username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth_["status"]:
        response["message"] = auth_["message"]
        return jsonify(response), response_codes["auth_error"]
    if currency not in Currencies.currencies:
        response["message"] = "Invalid currency"
        return jsonify(response), response_codes["bad_request"]
    data = query.currency_convert_all(currency)
    if not data["status"]:
        response["message"] = data["message"]
        return jsonify(response), response_codes["unrecognized"]
    
    response["status"] = "ok"
    response["message"] = "Successful"
    response["data"] = data["data"]
    return jsonify(response), response_codes["ok"]


@app.route("/api/<currency>/last-updated/", methods = ["GET"])
def currency_last_updated(currency):
    currency = currency.upper()
    response = {"status": "error", "message": "", "data": {}}
    try:
        data = request.get_json()
    except:
        response["message"] = "Invalid request"
        return jsonify(response), response_codes["bad_request"]
    if "username" not in data or "password" not in data:
        response["message"] = "Please provide you r username and password"
        return jsonify(response), response_codes["auth_error"]
    auth_ = auth_user.auth(data["username"], data["password"])
    if not auth_["status"]:
        response["message"] = auth_["message"]
        return jsonify(response), response_codes["auth_error"]
    if currency not in Currencies.currencies:
        response["message"] = "Invalid currency"
        return jsonify(response), response_codes["bad_request"]
    details = query.currency_details(currency)
    if not details["status"]:
        response["message"] = details["message"]
        return jsonify(response), response_codes["unavailable"]
    response["data"]["date"] = details["data"]["date"]
    response["data"]["time"] = details["data"]["time"]
    response["data"]["timezone"] = details["data"]["timezone"]
    return jsonify(response), response_codes["ok"]
