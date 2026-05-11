# Vectorised Backtesting

## Key Terms

- **Vectorised backtest**: Backtest using column operations, not trade-by-trade simulation.
- **Cumulative return**: Compounded growth from periodic returns.

## Core Explanation

Vectorised backtesting multiplies market returns by position series:

- `strategy_return = log_return * position`
- Cumulative strategy equity from cumulative sum and exponentiation.

This approach is fast and suitable for prototype analysis.

## Worked Example

`backtesting/vectorised_backtest.py` calculates strategy return, annual metrics, drawdown, and comparison tables across strategies.

## Command Reference Or Code Pattern

```python
result["strategy_return"] = result["log_return"] * result["position"]
result["cumret_strategy"] = result["strategy_return"].cumsum().apply(np.exp)
rolling_max = result["cumret_strategy"].cummax()
drawdown = (result["cumret_strategy"] - rolling_max) / rolling_max
```

## Advanced

### Deeper Concepts
- Vectorized backtesting is fast and ideal for research, but simplifying assumptions can obscure path-dependent execution realities.
- Validate vectorized logic with small hand-checkable examples before scaling to full datasets.
- Separate signal math from portfolio accounting to improve testability and transparency.
- Use benchmark checks against event-driven simulations for strategies sensitive to order timing.

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
- Build a vectorized backtester with modular signal and performance components.
- Validate vectorized outputs against a manually computed small sample.
- Compare results to an event-driven prototype for one strategy.
