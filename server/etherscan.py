
import requests
import os
import math

import server.binance as binance

ETHERSCAN_API_KEY = "ETHERSCAN_API_KEY"
ETHERSCAN_API_URL = "https://api.etherscan.io/api" 


def get_internal_transaction_list_by_hash(hash):
    key = os.getenv(ETHERSCAN_API_KEY)
    
    payload = {
        "module": "account",
        "action": "txlistinternal",
        "txhash": hash,
        "apikey": key
    }

    resp = requests.get(ETHERSCAN_API_URL, payload)
    data = resp.json()
    return data["result"] # List of structs


def get_internal_transaction_list_by_hash_batch(hashlist):
    result_data = {}
    for h in hashlist:
        result_data[h] = get_internal_transaction_list_by_hash(h)
        
    return result_data


def get_token_transfer_fee_by_hash_batch(results):
    final_result = []

    for key, val in results.items():
      fee = get_token_transfer_fee_by_hash(val, key)
      final_result += fee

    return final_result


def get_token_transfer_fee_by_hash(results, hash):
    for data in results:
        timestampMilliSecond = unix_second_to_unix_millisecond(data["timeStamp"])
        price = binance.get_price_by_timestamp(timestampMilliSecond)
        result = []

        tokenListJson = get_token_transfer_by_address(data)
        for r in tokenListJson["result"]:
            # By right there should only be one value here
            if r["hash"] == hash and r["tokenSymbol"] == "WETH":
                fee = calculate_transaction_fee_in_eth(r["gasPrice"], r["gasUsed"], r["tokenDecimal"])
                resultData = {
                    "txn hash": hash,
                    "block number": r["blockNumber"],
                    "timestamp": r["timeStamp"],
                    "fee in ETH": fee,
                    "closing price in usdt": price,
                    "transaction_fee in usdt": str(fee * float(price))
                }
                    
                result.append(resultData)

    return result


def get_token_transfer_by_address(data):
    key = os.getenv(ETHERSCAN_API_KEY)

    tokenPayload = {
        "module": "account",
        "action": "tokentx",
        "address":  data["from"],
        "apikey": key,
        "startblock": data["blockNumber"],
        "endblock": data["blockNumber"],
        "sort": "asc"
    }

    if data["contractAddress"] != "":
        tokenPayload["contractAddress"] = data["contractAddress"]

    resp = requests.get(ETHERSCAN_API_URL, tokenPayload)
    return resp.json()


def calculate_transaction_fee_in_eth(gas_price: str, gas_used: str, token_decimal: str):
    return int(gas_price) * math.pow(10, -1 * int(token_decimal)) * int(gas_used)

def unix_second_to_unix_millisecond(s):
    return s + "000"