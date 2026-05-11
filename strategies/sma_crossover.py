import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Support both script execution and interactive notebook contexts.
try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path.cwd().resolve()
    PROJECT_ROOT = cwd.parent if cwd.name == "strategies" else cwd
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import df

def sma_crossover(df, fast=20, slow=50):
    """ SMA Crossover Strategy
    
    Parameters:
        df: pandas DataFrame with 'close' prices
        fast: window for short SMA
        slow: window for long SMA
    
    Returns:
        DataFrame with 'signal' column (1 for buy, -1 for sell, 0 for hold)
    """

    df = df.copy()

    #Calculate moving averages
    df[f"SMA_{fast}"] = df["close"].rolling(window=fast).mean()
    df[f"SMA_{slow}"] = df["close"].rolling(window=slow).mean()

    #Signal: 1 if fast SMA crosses above slow SMA, -1 if fast SMA crosses below slow SMA, 0 otherwise
    df["signal"] = np.where(df[f"SMA_{fast}"] > df[f"SMA_{slow}"], 1, np.where(df[f"SMA_{fast}"] < df[f"SMA_{slow}"], -1, 0))

    # Position: shift signal forward by 1 day.
    # This avoids look-ahead bias by entering on the next bar.
    df["position"] = df["signal"].shift(1)

    return df

#Apply the strategy to the data
FAST_WINDOW = 20
SLOW_WINDOW = 50
df_sma = sma_crossover(df, fast=FAST_WINDOW, slow=SLOW_WINDOW)

df_sma.to_csv("data/sma_crossover.csv", index=False)

#Inspect the signals
print(df_sma[["close", f"SMA_{FAST_WINDOW}", f"SMA_{SLOW_WINDOW}", "signal", "position"]].tail())

#Visualising the Signals
def plot_sma_signals(df, fast=20, slow=50):
    fig, ax = plt.subplots(figsize=(14, 6))

    #Price and moving averages
    ax.plot(df_sma.index, df_sma["close"], linewidth=0.8, label="Close Price", color="steelblue", zorder=2)
    ax.plot(df_sma.index, df_sma[f"SMA_{fast}"], linewidth=1.2, label=f"SMA_{fast}", color="orange", zorder=3)
    ax.plot(df_sma.index, df_sma[f"SMA_{slow}"], linewidth=1.2, label=f"SMA_{slow}", color="red", zorder=3)

    # Crossover markers: regime changed vs previous bar.
    # `signal` is current bull/bear (+1/-1); `position` is yesterday's signal (shift(1)).
    # Wrong filter was `position == 0`: that only catches flat→bull/bear, not short↔long.
    bullish_cross = (df_sma["signal"] == 1) & (df_sma["position"] != 1)
    bearish_cross = (df_sma["signal"] == -1) & (df_sma["position"] != -1)
    buy_signals = df_sma[bullish_cross]
    ax.scatter(buy_signals.index, buy_signals["close"], marker="^", color="green", s=80, label="Buy", zorder=4)

    sell_signals = df_sma[bearish_cross]
    ax.scatter(sell_signals.index, sell_signals["close"], marker="v", color="red", s=80, label="Sell", zorder=4)
    
    #Other plot settings
    ax.set_title(f"SMA Crossover Strategy - Fast={fast}, Slow={slow} - BTC/USDT")
    ax.set_ylabel("Price (USDT)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print(f"Total Buy Signals: {len(buy_signals)}")
    print(f"Total Sell Signals: {len(sell_signals)}")

plot_sma_signals(df_sma, fast=FAST_WINDOW, slow=SLOW_WINDOW)