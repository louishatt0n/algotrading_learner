# pandas

## Key Terms

- **DataFrame**: 2D labeled table.
- **Index**: Row labels, often dates in time-series analysis.
- **Vectorized operation**: Column-wise computation without manual loops.

## What It Is

pandas is a data analysis library for tabular and time-series data.

## Why It Is Used

In this project, pandas handles:

- OHLCV data loading from CSV.
- Time-indexed slicing.
- Indicator columns (SMA, momentum, z-score).
- Backtest metric aggregation.

## Useful Commands

```python
import pandas as pd
df = pd.read_csv("data/btc_daily.csv", index_col="date", parse_dates=True)
df.head()
df.tail()
df.describe()
df["close"].rolling(window=20).mean()
df.dropna(subset=["position", "log_return"])
```

## Useful Commands With Examples

```python
# Create log return column
import numpy as np
df["log_return"] = np.log(df["close"] / df["close"].shift(1))

# Filter rows where strategy is in market
in_market = df[df["position"] != 0]

# Sort parameter search output by Sharpe
best = grid_results.sort_values(by="sharpe", ascending=False).head(5)
```

## Advanced

### Deeper Concepts
- Think in terms of tabular semantics: each column has meaning, type, and quality constraints that influence downstream calculations.
- Master index behavior and alignment rules; many subtle bugs arise from unintended index alignment during arithmetic and merges.
- Choose transformation patterns deliberately (`assign`, `groupby`, `pivot`, `merge`) to keep data pipelines readable and testable.
- Treat missing data handling as a modeling decision, not merely a cleaning step.

### Free Platforms and Courses
- [pandas documentation](https://pandas.pydata.org/docs/) for authoritative API and user-guide coverage.
- [Python docs](https://docs.python.org/3/) for language features that improve data pipeline code quality.
- [CS50 Python](https://cs50.harvard.edu/python) for reinforcing core programming concepts used in analysis scripts.
- [Khan Academy finance](https://www.khanacademy.org/economics-finance-domain/core-finance) for contextual datasets and financially meaningful metrics.

### Practice Path
- Create a notebook that loads messy CSV data, enforces types, and logs each cleaning decision with rationale.
- Build a small reusable function library for common transformations (date parsing, outlier clipping, grouped aggregates).
- Compare two equivalent analyses using method chaining versus stepwise variables and evaluate clarity.
- Add lightweight assertions after each major transformation to catch schema drift early.

### Suggested Mini-Projects
- Analyze a free market dataset and produce a concise report with cleaned tables and interpretable metrics.
- Implement a data-quality audit script that flags null spikes, duplicate keys, and unexpected category changes.
- Build an end-to-end pandas workflow from raw ingest to exportable summary tables for a trading strategy prototype.
