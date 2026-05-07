from binance.client import Client
client = Client()

#Get the current BTC/USDT price
ticker = client.get_symbol_ticker(symbol="BTCUSDT")
print(f"BTC/USDT: {ticker['price']}")