# SMA Crossover

## Key Terms

- **SMA**: Simple moving average.
- **Crossover**: Fast average crossing slow average.
- **Look-ahead bias**: Using future information by mistake.

## Core Explanation

SMA crossover compares short-term trend (`fast`) with long-term trend (`slow`):

- Fast > Slow: bullish regime.
- Fast < Slow: bearish regime.

Shifted position (`signal.shift(1)`) delays execution to next bar and avoids look-ahead bias.

## Worked Example

`strategies/sma_crossover.py` computes `SMA_fast`, `SMA_slow`, `signal`, and `position`, then visualizes buy/sell transitions.

## Command Reference Or Code Pattern

```python
df[f"SMA_{fast}"] = df["close"].rolling(window=fast).mean()
df[f"SMA_{slow}"] = df["close"].rolling(window=slow).mean()
df["signal"] = np.where(df[f"SMA_{fast}"] > df[f"SMA_{slow}"], 1, -1)
df["position"] = df["signal"].shift(1)
```

## Advanced

### Deeper Concepts
- Moving-average crossovers encode trend-following assumptions; lag and whipsaw behavior should be measured explicitly rather than assumed.
- Parameter choices (lookback windows) form a hypothesis space, not a guarantee of profitability.
- Signal generation must be separated from execution assumptions to avoid hidden look-ahead bias.
- Risk management and transaction costs often dominate headline return metrics.

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
- Implement a crossover strategy with walk-forward parameter testing and realistic fees.
- Compare strategy outcomes across trending and range-bound market regimes.
- Build a report separating raw signal quality from execution-adjusted performance.
