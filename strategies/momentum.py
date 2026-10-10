#Simple basis: assets that have been performing well recently are likely to continue performing well in the future
#The strategy looks at the returns over the last N days, and enters a position if the return is positive
#The strategy exits the position if the return is negative

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


def momentum_strategy(df, window=20):
    """ Momentum Strategy
    
    Parameters:
        df: pandas DataFrame with 'close' prices
        window: window for the momentum calculation
    
    Returns:
        DataFrame with 'signal' column (1 for buy, -1 for sell, 0 for hold)
    """
    
    df = df.copy()

    #Momentum: cumulative log return over the last N days
    df["momentum"] = np.log(df["close"] / df["close"].shift(window))

    #Signal: 1 if momentum is positive, -1 if momentum is negative, 0 otherwise
    df["signal"] = np.where(df["momentum"] > 0, 1, np.where(df["momentum"] < 0, -1, 0))

    #Position: shift signal forward by 1 day
    df["position"] = df["signal"].shift(1)

    return df

#Apply the strategy to a 20-day window
if __name__ == "__main__":
    from src.data_loader import load_prices
    df = load_prices()

    df_momentum = momentum_strategy(df, window=20)

    print(df_momentum[["close", "momentum", "signal", "position"]].tail(10))

    #Visualising the Signals
    def plot_momentum(df_momentum, window=20):
        fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={'height_ratios': [2, 1]})

        #Price with position shading
        axes[0].plot(df_momentum.index, df_momentum["close"], linewidth=0.8, label="Close Price", color="steelblue", zorder=2)

        #Position shading: green for long, red for short
        long_positions = df_momentum[df_momentum["position"] == 1]
        axes[0].fill_between(long_positions.index, long_positions["close"], color="green", alpha=0.1, label="Long")
        short_positions = df_momentum[df_momentum["position"] == -1]
        axes[0].fill_between(short_positions.index, short_positions["close"], color="red", alpha=0.1, label="Short")

        axes[0].set_title(f"Momentum Strategy - {window}-day Window - BTC/USDT")
        axes[0].set_ylabel("Price (USDT)")
        axes[0].legend(loc="best")
        axes[0].grid(True, alpha=0.3)

        #Momentum Line
        axes[1].plot(df_momentum.index, df_momentum["momentum"], linewidth=1.2, label="Momentum", color="purple", zorder=3)
        axes[1].axhline(0, color="black", linestyle="--", linewidth=1, zorder=4)
        axes[1].fill_between(df_momentum.index, df_momentum["momentum"], where=df_momentum["momentum"] > 0, color="green", alpha=0.1, label="Positive Momentum")
        axes[1].fill_between(df_momentum.index, df_momentum["momentum"], where=df_momentum["momentum"] < 0, color="red", alpha=0.1, label="Negative Momentum")
        axes[1].set_ylabel("Momentum")
        axes[1].legend(loc="best")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    plot_momentum(df_momentum, window=20)

    #Compare different windows
    for window in [10, 20, 30, 40, 50]:
        df_temp = momentum_strategy(df, window=window)
        in_market_pct = (df_temp["position"] != 0).mean()
        print(f"Window {window}: {in_market_pct:.2%} in market")