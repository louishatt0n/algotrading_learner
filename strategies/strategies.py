"""
strategies.py -- Classic trading strategies
"""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path.cwd().resolve()
    PROJECT_ROOT = cwd.parent if cwd.name == "strategies" else cwd
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def sma_crossover_strategy(df, fast=20, slow=50):
    """SMA Crossover: buy when fast SMA is above slow SMA."""
    df = df.copy()
    df[f"SMA_{fast}"] = df["close"].rolling(window=fast).mean()
    df[f"SMA_{slow}"] = df["close"].rolling(window=slow).mean()
    df["signal"] = np.where(df[f"SMA_{fast}"] > df[f"SMA_{slow}"], 1, 0)
    df["position"] = df["signal"].shift(1)
    return df


def momentum_strategy(df, window=20):
    """Momentum: buy when cumulative return over N days is positive."""
    df = df.copy()
    df["momentum"] = np.log(df["close"] / df["close"].shift(window))
    df["signal"] = np.where(df["momentum"] > 0, 1, 0)
    df["position"] = df["signal"].shift(1)
    return df


def mean_reversion_strategy(df, window=20, threshold=-1.0):
    """Mean Reversion: buy when z-score is below threshold."""
    df = df.copy()
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    df["rolling_std"] = df["close"].rolling(window=window).std()
    df["zscore"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]
    df["signal"] = np.where(df["zscore"] < threshold, 1, 0)
    df["position"] = df["signal"].shift(1)
    return df


if __name__ == "__main__":
    from src.data_loader import df as ohlc

    fast, slow = 20, 50
    sma = sma_crossover_strategy(ohlc, fast=fast, slow=slow)
    print("SMA crossover (tail):")
    print(sma[["close", f"SMA_{fast}", f"SMA_{slow}", "signal", "position"]].tail(5))

    mom = momentum_strategy(ohlc, window=20)
    print("\nMomentum (tail):")
    print(mom[["close", "momentum", "signal", "position"]].tail(5))

    mr = mean_reversion_strategy(ohlc, window=20, threshold=-1.0)
    print("\nMean reversion (tail):")
    print(mr[["close", "rolling_mean", "rolling_std", "zscore", "signal", "position"]].tail(5))
