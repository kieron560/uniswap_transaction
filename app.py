from flask import Flask
from flask import jsonify
from flask import request
import json

from dotenv import load_dotenv
import server.etherscan as etherscan
import asyncio
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
swagger = Swagger(app)


@app.route("/transaction_fee_single", methods=['GET'])
def get_transaction_fee():
    hash = request.args.get("hash")
    if hash is None or hash == "":
        return ""
    
    internal_transaction_list = etherscan.get_internal_transaction_list_by_hash([hash])
    result = etherscan.get_token_transfer_fee_by_hash(internal_transaction_list, hash)

    return jsonify(result)

@app.route("/transaction_fee_batch", methods=['POST'])
def get_transaction_fee_batch():
    hash = request.get_json()["hash"]
    if hash is None or len(hash) == 0:
        return "helllooo"
    
    # concurrent api calls to get the transaction fee for each hash
    internal_transaction_list = etherscan.get_internal_transaction_list_by_hash_batch(hash)
    result = etherscan.get_token_transfer_fee_by_hash_batch(internal_transaction_list, hash)

    return jsonify(result)


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
