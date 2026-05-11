#Mean reversion is the opposite of momentum: if the price has deviated significantly from its mean, it is likely to revert
#Deviation is measured used a Z-score: (price - mean) / sigma
#If Z < -1, the price is significantly below the mean, and we enter a long position
#If Z > 0, the price returned to the mean, and we enter a short position

import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Support both script execution and interactive contexts; load OHLC data.
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path.cwd().resolve()
    PROJECT_ROOT = cwd.parent if cwd.name == "strategies" else cwd
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import df

def mean_reversion_strategy(df, window=20, threshold=-1.0, exit_z=0.0):
    """ Mean Reversion Strategy based on Z-score
    
    Parameters:
        df: pandas DataFrame with 'close' prices
        window: window for the Z-score calculation
        threshold: enter long when z_score is below this (e.g. -1 = unusually cheap vs window)
        exit_z: enter short / take opposite side when z_score is above this (e.g. back above mean)
    
    Returns:
        DataFrame with 'signal' column (1 for buy, -1 for sell, 0 for hold)
    """
    
    df = df.copy()

    #Rolling mean and standard deviation
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df["rolling_std"] = df["close"].rolling(window=window).std()

    #Z-score: (price - mean) / sigma
    df["z_score"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]

    # Signal: long when Z is below threshold; short when Z is above exit_z; else neutral
    df["signal"] = np.where(
        df["z_score"] < threshold,
        1,
        np.where(df["z_score"] > exit_z, -1, 0),
    )

    #Position: shift signal forward by 1 day
    df["position"] = df["signal"].shift(1)

    return df

#Apply the strategy to the data
df_mr = mean_reversion_strategy(df, window=20, threshold=1)

print(df_mr[["close", "rolling_mean", "rolling_std", "z_score", "signal", "position"]].tail(10))

#Understanding Z-score in practice
print("Z-score statistics:")
print(df_mr["z_score"].describe())

#How often does the price fall below different thresholds?
for thresh in [-.5, -1, -1.5, -2]:
    pct = (df_mr["z_score"] < thresh).mean()*100
    print(f"Z-score < {thresh:.1f}: {pct:.1f}%")


#Visualising the Signals
def plot_mean_reversion(df_mr, window=20, threshold=1.0, exit_z=0.0):
    fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    axes[0].set_title(f"Mean Reversion Strategy - {window}-day Window - BTC/USDT")
    axes[0].set_ylabel("Price (USDT)")

    #Price and rolling mean
    axes[0].plot(df_mr.index, df_mr["close"], linewidth=0.8, label="Close Price", color="steelblue", zorder=2)
    axes[0].plot(df_mr.index, df_mr["rolling_mean"], linewidth=1.2, label=f"SMA {window}", color="orange", zorder=3)

    #+/- 1 and 2 standard deviation bands
    axes[0].fill_between(df_mr.index, df_mr["rolling_mean"] + df_mr["rolling_std"], df_mr["rolling_mean"] - df_mr["rolling_std"], color="gray", alpha=0.1, label="1 Std Dev")
    axes[0].fill_between(df_mr.index, df_mr["rolling_mean"] + 2*df_mr["rolling_std"], df_mr["rolling_mean"] - 2*df_mr["rolling_std"], color="red", alpha=0.1, label="2 Std Dev")

    axes[1].plot(df_mr.index, df_mr["z_score"], linewidth=0.8, color="purple", label="Z-score")
    axes[1].axhline(0, color="black", linewidth=0.8, linestyle="--")
    axes[1].axhline(threshold, color="green", linewidth=1, linestyle="--", label=f"Threshold ({threshold})")
    axes[1].axhline(-threshold, color="red", linewidth=1, linestyle="--")
    axes[1].fill_between(df_mr.index, threshold, df_mr["z_score"], where=df_mr["z_score"] < threshold, alpha=0.3, color="green", label="Buy zone")
    axes[1].set_ylabel("Z-score")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

plot_mean_reversion(df_mr, window=20, threshold=1, exit_z=0.0)