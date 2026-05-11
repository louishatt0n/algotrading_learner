# Parameter Optimisation

## Key Terms

- **Grid search**: Evaluate all parameter combinations in chosen ranges.
- **Overfitting**: Tuning to historical noise rather than robust signal.

## Core Explanation

Optimization can improve results, but must be disciplined:

- Define valid parameter ranges.
- Measure out-of-sample performance.
- Prefer robust regions over single extreme best point.

## Worked Example

`backtesting/event_driven.py` performs SMA grid search and walk-forward analysis to estimate out-of-sample behavior.

## Command Reference Or Code Pattern

```python
for fast in fast_range:
    for slow in slow_range:
        if fast >= slow:
            continue
        df_strat = sma_crossover.sma_crossover(ohlc, fast=fast, slow=slow)
```

## Advanced

### Deeper Concepts
- Optimization should target robust parameter regions, not single-point maxima that usually reflect noise.
- Use nested validation and walk-forward testing to reduce overfitting.
- Sensitivity analysis reveals whether performance depends on fragile parameter tuning.
- Prefer interpretable parameter priors grounded in market logic over blind brute-force searches.

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
- Run grid and random search with walk-forward validation and compare stability.
- Visualize parameter surfaces and identify broad stable plateaus.
- Create an overfitting checklist applied to every optimization run.
