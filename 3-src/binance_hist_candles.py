import pandas as pd
from binance.client import Client

client = Client()

klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "2 years ago UTC")

columns = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "trades",
    "taker_buy_base",
    "taker_buy_quote",
    "ignore"
]

#Create a DataFrame
df = pd.DataFrame(klines, columns=columns)
print(f"downloaded {len(df)} candles")

#Convert types
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

for col in ["open", "high", "low", "close", "volume"]:
    df[col] = df[col].astype(float)

#Set the timestamp as the index
df.set_index('open_time', inplace=True)
df.index.name = 'date'

#Keep only the columns we need
df = df[["open", "high", "low", "close", "volume"]]

#Print the last 5 rows
print(df.tail())

#Print the period and total candles
print(f"Period: {df.index[0].date()} -- {df.index[-1].date()}")
print(f"Total candles: {len(df)}")


#Print the descriptive statistics
print(df.describe())

#Print the information about the DataFrame
df.info()

#Print the columns of the DataFrame
print(df.columns)

#Print the index of the DataFrame
print(df.index)

#Data for a specific periods
df_2024 = df.loc["2024"]
df_q1_2024 = df_2024["2024-01-01":"2024-03-31"]
df_on_2024_06_15 = df.loc["2024-06-15"]
df_last_30_days = df.tail(30)

print("2024 sample:")
print(df_2024.head())
print("Q1 2024 sample:")
print(df_q1_2024.head())
print("Candle on 2024-06-15:")
print(df_on_2024_06_15)
print("Last 30 days sample:")
print(df_last_30_days.head())