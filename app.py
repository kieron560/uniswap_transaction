import math
from flask import Flask
from flask import jsonify
from flask import request
import json
import server.constants as constants

import requests
import os
from dotenv import load_dotenv
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
swagger = Swagger(app)


@app.route("/transaction_fee")
def get_transaction_fee():
    hash = request.args.get("hash")
    if hash is None:
        return ""
    
    internal_transaction_list = get_internal_transaction_list_by_hash(hash)
    result = get_token_transfer_fee_by_hash(internal_transaction_list, hash)

    return jsonify(result)


def get_internal_transaction_list_by_hash(hash):
    key = os.getenv(constants.ETHERSCAN_API_KEY)
    
    payload = {
        "module": "account",
        "action": "txlistinternal",
        "txhash": hash,
        "apikey": key
    }

    resp = requests.get(constants.ETHERSCAN_API_URL, payload)
    data = resp.json()
    return data["result"]


def get_token_transfer_fee_by_hash(results, hash):
    key = os.getenv(constants.ETHERSCAN_API_KEY)

    for data in results:
        timestamp = data["timeStamp"]
        blockNumber = data["blockNumber"]
        address = data["from"]
        contractAddress = data["contractAddress"]

        tokenPayload = {
            "module": "account",
            "action": "tokentx",
            "address": address,
            "apikey": key,
            "startblock": blockNumber,
            "endblock": blockNumber,
            "sort": "asc"
        }

        pricePayload = {
            "symbol": constants.ETH_USDT_SYMBOL,
            "interval": "1s",
            "startTime": unix_second_to_unix_millisecond(timestamp),
            "endTime": unix_second_to_unix_millisecond(timestamp),
        }

        if contractAddress != "":
            tokenPayload["contractAddress"] = contractAddress


        priceResp = requests.get(constants.BINANCE_KLINES_API_URL, pricePayload)
        priceData = priceResp.json()
        price = priceData[0][4] # index 4 is the closing price

        resp = requests.get(constants.ETHERSCAN_API_URL, tokenPayload)
        respData = resp.json()
        for r in respData["result"]:
            if r["hash"] == hash and r["tokenSymbol"] == "WETH":
                fee = calculate_transaction_fee_in_eth(r["gasPrice"], r["gasUsed"], r["tokenDecimal"])
                feeInUSDT = fee * float(price)
                return feeInUSDT


def calculate_transaction_fee_in_eth(gas_price: str, gas_used: str, token_decimal: str):
    return int(gas_price) * math.pow(10, -1 * int(token_decimal)) * int(gas_used)


def unix_second_to_unix_millisecond(s):
    return s + "000"


# Configure Swagger UI for display
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    print()
    with open('docs/swagger.json', 'r') as f:
        return jsonify(json.load(f))


if __name__ == "__main__":
    load_dotenv()
    print(("* Loading model and Flask starting server..."
           "please wait until server has fully started"))
    app.run(debug=True)
