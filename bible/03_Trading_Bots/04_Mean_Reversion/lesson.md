# Mean Reversion

## Key Terms

- **Rolling mean**: Local average over lookback window.
- **Z-score**: Standardized deviation from mean.

## Core Explanation

Mean reversion assumes extreme deviations may move back toward average.  
Z-score measures distance from rolling mean in standard deviation units.

- Enter long when z-score is sufficiently low.
- Exit or reverse when z-score reverts above chosen level.

## Worked Example

`strategies/mean_reversion.py` computes rolling mean/std, z-score, and signal via threshold logic.

## Command Reference Or Code Pattern

```python
df["rolling_mean"] = df["close"].rolling(window=20).mean()
df["rolling_std"] = df["close"].rolling(window=20).std()
df["z_score"] = (df["close"] - df["rolling_mean"]) / df["rolling_std"]
df["signal"] = np.where(df["z_score"] < -1, 1, np.where(df["z_score"] > 0, -1, 0))
```

## Advanced

### Deeper Concepts
- Mean reversion assumptions depend on stationarity and regime context; they are not universally valid.
- Entry and exit thresholds should be calibrated against noise, spread behavior, and execution frictions.
- Half-life estimation and z-score scaling help connect intuition to statistically grounded timing.
- Risk controls must address tail events where reversion fails and trends persist.

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
- Backtest a z-score mean reversion model with regime filters and stop-loss controls.
- Estimate and compare mean-reversion half-life across multiple instruments.
- Create a stress-test suite for non-reverting periods.
