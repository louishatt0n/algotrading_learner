# Event-Driven Backtesting

## Key Terms

- **Event-driven**: Logic reacts to each time-step event.
- **Portfolio state**: Current cash, position, and equity.

## Core Explanation

Event-driven backtesting simulates execution sequentially:

1. Read next bar.
2. Apply signal decision.
3. Execute buy/sell with costs/slippage.
4. Record updated equity.

It is slower than vectorised methods but more realistic.

## Worked Example

`backtesting/event_driven.py` uses a `Portfolio` class with `buy`, `sell`, `record`, and `run_backtest` to simulate trading path.

## Command Reference Or Code Pattern

```python
if position == 1:
    portfolio.buy(price, date)
elif position <= 0:
    portfolio.sell(price, date)
portfolio.record(date, price)
```

## Advanced

### Deeper Concepts
- Event-driven frameworks model order lifecycle and market microstructure more faithfully than purely vectorized methods.
- A robust architecture separates data events, signal events, order events, and fill events.
- Latency, slippage, and partial fills should be treated as model parameters, not ignored edge cases.
- State management and deterministic replay are essential for debugging strategy behavior.

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
- Implement a minimal event loop with explicit event classes and logging.
- Model slippage and partial fills, then quantify their impact against idealized fills.
- Add deterministic replay tests to verify reproducibility of trade decisions.
