from binance.client import Client
client = Client()

#Or with API key and secret key (needed for trading)
#client = Client(api_key="YOUR_API_KEY", api_secret="YOUR_API_SECRET")

#Get the current BTC/USDT price
ticker = client.get_symbol_ticker(symbol="BTCUSDT")
print(f"BTC/USDT: {ticker['price']}")