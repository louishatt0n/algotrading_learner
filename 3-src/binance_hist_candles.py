import pandas as pd
from binance.client import Client

client = Client()

#Download daily BTC/USDT candles for the last 2 years
klines = client.get_historical_klines(
    symbol="BTCUSDT", 
    interval=Client.KLINE_INTERVAL_1DAY, 
    start_str="2 years ago UTC")

#Binance allows you to request candles at different intervals
#The most common are 1 minute, 5 minutes, 15 minutes, 30 minutes, 1 hour, 4 hours, 1 day
#We can use the Client.KLINE_INTERVAL_1MINUTE, Client.KLINE_INTERVAL_5MINUTE, Client.KLINE_INTERVAL_15MINUTE, Client.KLINE_INTERVAL_30MINUTE, Client.KLINE_INTERVAL_1HOUR, Client.KLINE_INTERVAL_4HOUR, Client.KLINE_INTERVAL_1DAY
#For example, to get the last 1000 candles at 1 minute interval, we can use:
#klines = client.get_historical_klines(
#    symbol="BTCUSDT", 
#    interval=Client.KLINE_INTERVAL_1MINUTE, 
#    start_str="1000 minutes ago UTC")

#Binance API returns a list of lists, each containing 1000 candles
#We need to convert this list of lists into a DataFrame
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
#Raw data from Binance comes with Unix timestamps in milliseconds and prices as strings
#We need to convert them to datetime (for practical use) and float (for numerical operations)
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

#WORKING WITH THE DATA============================================================================================================================>
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

#Filtering the data
#Days when BTC was above $60000
df_above_60k = df[df["close"] > 60000]
print(f"BTC was above $60000 for {len(df_above_60k)} days")

#Days with above average volume
avg_volume = df["volume"].mean()
df_high_volume = df[df["volume"] > avg_volume]
print(f"Days with above average volume: {len(df_high_volume)}")

#Resampling
#Resampling is the process of converting a time series into a lower frequency
#Turn daily candles into weekly candles
df_weekly = df.resample("W").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})
print(df_weekly.head())

#Resampling to a different frequency
#Turn daily candles into monthly candles
df_monthly = df.resample("ME").agg({
    "open": "first",
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
})
print(df_monthly.head())

#CALCULATING RETURNS============================================================================================================================>
#Simple Returns
df["simple_return"] = df["close"].pct_change()
print(df[["close", "simple_return"]].head())

#Log Returns
#Log returns have an important property: they are additive: the sum of the log returns = the log return over the entire period
import numpy as np

df["log_return"] = np.log(df["close"] / df["close"].shift(1))
print(df["log_return"].head())

#Cumulative Returns show how an investment has grown over time
#Cumulative Return
df["cumulative_return"] = df["log_return"].cumsum().apply(np.exp)-1

#Total Returns
total_return = df["log_return"].iloc[-1]
print(f"Total return: {total_return}")

#VISUALIZING THE DATA============================================================================================================================>
import matplotlib.pyplot as plt
#Price Chart 
#fig, ax = plt.subplots(figsize=(12, 5))
#ax.plot(df.index, df["close"], linewidth=0.8, color = "steelblue", label = "BTC/USDT")
#ax.set_title("BTC/USDT - Daily Close Price")
#ax.set_xlabel("Date")
#ax.set_ylabel("Price (USDT)")   
#ax.grid(True, linestyle = "--", alpha = 0.3)
#plt.tight_layout()

#Return Distribution
fig, ax = plt.subplots(figsize=(10, 5))
log_returns = df["log_return"].dropna()
counts, bins, _ = ax.hist(
    log_returns,
    bins=100,
    color="steelblue",
    edgecolor="white",
    alpha=0.8,
)

# Overlay a fitted normal distribution line.
mu = log_returns.mean()
sigma = log_returns.std()
x = np.linspace(log_returns.min(), log_returns.max(), 300)
bin_width = bins[1] - bins[0]
normal_pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
ax.plot(x, normal_pdf * len(log_returns) * bin_width, color="crimson", linewidth=2, label="Normal fit")
ax.axvline(0, color = "black", linestyle = "--", linewidth = 1)
ax.set_title("Distribution of Daily Log Returns - BTC/USDT")
ax.set_xlabel("Log Return")
ax.set_ylabel("Frequency")
ax.legend()
plt.tight_layout()

#Moving Averages on top of the price chart
df["SMA_20"] = df["close"].rolling(window=20).mean()
df["SMA_50"] = df["close"].rolling(window=50).mean()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df.index, df["close"], linewidth=0.8, color="steelblue", label="Close")
ax.plot(df.index, df["SMA_20"], linewidth=1, color="orange", label="SMA 20")
ax.plot(df.index, df["SMA_50"], linewidth=1, color="red", label="SMA 50")
ax.set_title("BTC/USDT with Moving Averages")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()


#Price chart with a trading volume graph beneath
fig, axes = plt.subplots(2, 1, figsize=(12, 7), gridspec_kw={"height_ratios": [3, 1]})
# Price
axes[0].plot(df.index, df["close"], linewidth=0.8, color="steelblue")
axes[0].set_title("BTC/USDT -- Price and Volume")
axes[0].set_ylabel("Price (USDT)")
axes[0].grid(True, alpha=0.3)
# Volume
axes[1].bar(df.index, df["volume"], color="gray", alpha=0.5, width=1)
axes[1].set_ylabel("Volume")
axes[1].grid(True, alpha=0.3)
plt.tight_layout()

#plt.show()


#STORING THE DATA============================================================================================================================>
#Downloading data from Binance every time is slow and wasteful. It is better to fetch it once and save it locally.
#The simplest and most universal format, CSV:
# Save
df.to_csv("6-data/btc_daily.csv")
# Load
df_loaded = pd.read_csv("6-data/btc_daily.csv", index_col="date", parse_dates=True)
print(df_loaded.head())

#For larger datasets, better to use HDF5:
# Save
df.to_hdf("6-data/btc_daily.h5", key="btc_daily", mode="w")
# Load
df_loaded = pd.read_hdf("6-data/btc_daily.h5", key="btc_daily")
print(df_loaded.head())