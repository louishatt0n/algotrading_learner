"""Download the full daily BTC/USDT price history from Binance's public market-data API.

No account or API key is needed. Binance returns at most 1,000 candles per request,
so we page forward from the first listing date until we reach today.

Usage (from the project root):
    python src/fetch_binance_daily.py            # writes data/btc_daily_full.csv
"""
import csv
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ENDPOINTS = [
    "https://data-api.binance.vision/api/v3/klines",  # public market-data mirror
    "https://api.binance.com/api/v3/klines",
]
SYMBOL = "BTCUSDT"
START_MS = int(datetime(2017, 8, 17, tzinfo=timezone.utc).timestamp() * 1000)  # BTCUSDT listing
OUT = Path(__file__).resolve().parents[1] / "data" / "btc_daily_full.csv"


def get(url):
    with urllib.request.urlopen(url, timeout=20) as r:
        return json.loads(r.read())


def fetch_all():
    rows, start = [], START_MS
    while True:
        query = f"?symbol={SYMBOL}&interval=1d&startTime={start}&limit=1000"
        for base in ENDPOINTS:
            try:
                batch = get(base + query)
                break
            except Exception as e:  # try the next endpoint
                last_error = e
        else:
            raise RuntimeError(f"all endpoints failed: {last_error}")
        if not batch:
            break
        rows.extend(batch)
        start = batch[-1][0] + 1          # next request starts after the last candle we got
        if len(batch) < 1000:
            break
        time.sleep(0.2)                   # be polite to the API
    return rows


def main():
    rows = fetch_all()
    today = datetime.now(timezone.utc).date()
    OUT.parent.mkdir(exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["date", "open", "high", "low", "close", "volume"])
        for k in rows:
            day = datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc).date()
            if day >= today:              # drop today's candle: it is still forming
                continue
            w.writerow([day.isoformat(), k[1], k[2], k[3], k[4], k[5]])
    print(f"wrote {OUT} ({len(rows)} candles fetched)")


if __name__ == "__main__":
    main()
