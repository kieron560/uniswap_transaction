import requests

BINANCE_KLINES_API_URL = "https://api.binance.com/api/v3/klines"
ETH_USDT_SYMBOL = "ETHUSDT"
CLOSING_PRICE_INDEX = 4

def get_price_by_timestamp(timestamp):
    pricePayload = {
        "symbol": ETH_USDT_SYMBOL,
        "interval": "1s",
        "startTime": timestamp,
        "endTime": timestamp,
    }
    priceResp = requests.get(BINANCE_KLINES_API_URL, pricePayload)
    priceData = priceResp.json()
    return priceData[0][CLOSING_PRICE_INDEX] # index 4 is the closing price