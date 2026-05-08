import numpy as np
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
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

    #Postion: shift signal forward by 1 day
    #(this is because we want to enter a position on the next day, after the crossover has occurred)
    df["position"] = df["signal"].shift(1)

    return df

#Apply the strategy to the data
FAST_WINDOW = 20
SLOW_WINDOW = 50
df_sma = sma_crossover(df, fast=FAST_WINDOW, slow=SLOW_WINDOW)

df_sma.to_csv("data/sma_crossover.csv")

#Inspect the signals
print(df_sma[["close", f"SMA_{FAST_WINDOW}", f"SMA_{SLOW_WINDOW}", "signal", "position"]].tail())