import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

# Crypto trades every day of the year, so annualise with 365 (stocks use ~252 trading days).
PERIODS_PER_YEAR = 365


def load_prices(filename="btc_daily_full.csv"):
    """Load daily BTC/USDT candles (date index) and add the daily log return.

    btc_daily_full.csv: Aug 2017 - Oct 2026, from src/fetch_binance_daily.py
    btc_daily.csv:      the original May 2024 - May 2026 sample
    """
    df = pd.read_csv(DATA_DIR / filename, index_col="date", parse_dates=True)
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    return df


if __name__ == "__main__":
    print(load_prices().head())
