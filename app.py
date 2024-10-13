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


@app.route("/transactions")
def get_transaction_fee_by_hash():
    key = os.getenv(constants.ETHERSCAN_API_KEY)
    hash = request.args.get("hash")
    if hash is None:
        return ""

    payload = {
        "module": "account",
        "action": "txlistinternal",
        "txhash": hash,
        "apikey": key
    }

    resp = requests.get(constants.ETHERSCAN_API_URL, payload)
    data = resp.json()
    return data


# Configure Swagger UI
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
