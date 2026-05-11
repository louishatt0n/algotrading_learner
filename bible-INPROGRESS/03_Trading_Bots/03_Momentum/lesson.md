# Momentum

## Key Terms

- **Momentum window**: Lookback period for return accumulation.
- **Positive momentum**: Recent net upward movement.

## Core Explanation

Momentum strategy assumes recent direction may continue.  
Compute rolling log-return over `N` days; use sign of momentum to determine long/short/flat signal.

## Worked Example

`strategies/momentum.py` computes:

- `momentum = log(close / close.shift(window))`
- `signal` from positive/negative momentum
- `position = signal.shift(1)`

## Command Reference Or Code Pattern

```python
df["momentum"] = np.log(df["close"] / df["close"].shift(window))
df["signal"] = np.where(df["momentum"] > 0, 1, np.where(df["momentum"] < 0, -1, 0))
df["position"] = df["signal"].shift(1)
```

## Advanced

### Deeper Concepts
- Momentum effects are horizon-dependent and can degrade under crowded positioning; robustness checks across assets and windows are critical.
- Normalize returns and volatility before ranking instruments to reduce concentration risk.
- Turnover control is a first-class design variable because high churn can erase gross alpha.
- Use out-of-sample evaluation and stability diagnostics to prevent overfitting momentum parameters.

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
- Construct a cross-sectional momentum ranking model with volatility scaling.
- Add turnover penalties and analyze net performance sensitivity.
- Run a robustness grid across lookback/holding horizons and document stability.
