import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data/btc_daily.csv", index_col="date", parse_dates=True)
df["log_return"] = np.log(df["close"] / df["close"].shift(1))

print(df.head())