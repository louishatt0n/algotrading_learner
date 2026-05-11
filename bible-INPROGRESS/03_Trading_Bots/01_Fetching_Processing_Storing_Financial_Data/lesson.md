# Fetching, Processing, and Storing Financial Data

## Key Terms

- **OHLCV**: Open, high, low, close, volume.
- **Resampling**: Changing data frequency (daily to weekly, etc.).
- **Persistence**: Saving processed data for reuse.

## Core Explanation

Your data workflow has three phases:

1. Fetch raw candles from source API.
2. Process data types, timestamps, and derived columns.
3. Store results to local files for reproducible downstream analysis.

## Worked Example

The script in `src/binance_hist_candles.py` fetches BTC/USDT candles, converts types, computes returns, and saves CSV/HDF outputs.

## Command Reference Or Code Pattern

```python
df = pd.read_csv("data/btc_daily.csv", index_col="date", parse_dates=True)
df["log_return"] = np.log(df["close"] / df["close"].shift(1))
df.to_csv("data/btc_daily.csv")
```

## Advanced

### Deeper Concepts
- Market data engineering requires explicit schema decisions: timestamps, timezone normalization, adjusted prices, and missing-value policies must be defined before modeling.
- Distinguish acquisition reliability (API limits, retries, version changes) from analytical reliability (cleaning rules, survivorship bias, corporate actions).
- Storage format influences research speed: columnar formats and partitioned datasets support reproducible, scalable backtests.
- Data lineage documentation is essential so signals can be traced back to raw sources.

### Free Platforms and Courses
- [QuantConnect documentation](https://www.quantconnect.com/docs) for production-grade algorithmic trading workflows and framework design.
- [QuantConnect training](https://www.quantconnect.com/docs/v2/cloud-platform/learning-center/training) for guided free practice modules.
- [freeCodeCamp algorithmic trading course](https://www.freecodecamp.org/news/algorithmic-trading-using-python-course/) for end-to-end practical implementation examples.
- [MIT Finance Theory I](https://ocw.mit.edu/courses/15-401-finance-theory-i-fall-2008/) for foundational asset-pricing and finance theory.
- [MIT Analytics of Finance](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/) for quantitative methods and analytical finance framing.
- [Yale Open Courses Financial Markets](https://oyc.yale.edu/economics/econ-252-08) for market-structure and institutional context.
- [Khan Academy finance](https://www.khanacademy.org/economics-finance-domain/core-finance) for concise reinforcement of core finance concepts.

### Practice Path
- Week 1: Reproduce one canonical strategy baseline with transparent assumptions, then document every metric and data source.
- Week 2: Add risk controls, transaction costs, and validation splits; compare net vs gross performance.
- Week 3: Run a robustness matrix across regimes, assets, and parameter ranges; identify stable regions.
- Week 4: Prepare a deployment-style report with hypothesis, method, limitations, and next experimental priorities.

### Suggested Mini-Projects
- Build a data ingestion pipeline with retry logic, schema validation, and timestamp normalization.
- Create a daily ETL job that stores OHLCV data and generates a data-quality report.
- Implement a reproducible dataset snapshot process for backtest versioning.
