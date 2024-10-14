from flask import Flask
from flask import jsonify
from flask import request
import json

from dotenv import load_dotenv
import server.etherscan as etherscan
from flasgger import Swagger
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)

@app.route("/transaction_fee_single", methods=['GET'])
def get_transaction_fee():
    hash = request.args.get("hash")
    if hash is None or hash == "":
        return "Hash cannot be empty", 404
    
    internal_transaction_list = etherscan.get_internal_transaction_list_by_hash([hash])
    result = etherscan.get_token_transfer_fee_by_hash(internal_transaction_list, hash)

    return jsonify(result), 200

@app.route("/transaction_fee_batch", methods=['POST'])
def get_transaction_fee_batch():
    hash = request.get_json()["hash"]
    if hash is None or len(hash) == 0:
        return "Hash cannot be empty", 404
    
    # concurrent api calls to get the transaction fee for each hash
    internal_transaction_map = etherscan.get_internal_transaction_list_by_hash_batch(hash)
    result = etherscan.get_token_transfer_fee_by_hash_batch(internal_transaction_map)

    return jsonify(result), 200

@app.route("/decode_transaction_swap", methods=['GET'])
def decode_transaction_swap():
    hash = request.get_json()["hash"]
    if hash is None or len(hash) == 0:
        return "Hash cannot be empty", 404
    
    # concurrent api calls to get the transaction fee for each hash
    internal_transaction_map = etherscan.get_internal_transaction_list_by_hash_batch(hash)
    result = etherscan.get_token_transfer_fee_by_hash_batch(internal_transaction_map)

    return jsonify(result), 200


# Configure Swagger UI for display
SWAGGER_URL = '/swagger'
API_URL = "/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Uniswap Transaction"
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
