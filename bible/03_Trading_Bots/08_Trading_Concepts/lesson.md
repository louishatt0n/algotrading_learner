# Trading Concepts

## Key Terms

- **Sharpe ratio**: Return per unit volatility.
- **Drawdown**: Peak-to-trough decline.
- **Win rate**: Fraction of positive outcomes.
- **Slippage**: Difference between expected and execution price.

## Core Explanation

Core concepts used across scripts:

- Return types: simple vs log.
- Risk-adjusted metrics: Sharpe, drawdown.
- Frictions: commissions and slippage.
- Exposure and time in market.
- In-sample vs out-of-sample distinction.

## Worked Example

Both `vectorised_backtest.py` and `event_driven.py` compare strategy return against buy-and-hold, then report risk and performance metrics.

## Command Reference Or Code Pattern

```python
annual_vol = result["strategy_return"].std() * np.sqrt(252)
sharpe = annual_return / annual_vol if annual_vol > 0 else 0
max_drawdown = drawdown.min()
```

## Advanced

### Deeper Concepts
- A complete trading system integrates signal, risk, execution, and monitoring; optimizing one component in isolation is insufficient.
- Strategy evaluation must combine return, risk, drawdown profile, capacity, and operational complexity.
- Behavioral and market-structure constraints influence whether theoretically sound models remain tradable.
- Governance and documentation quality are part of system performance in real deployment.

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
- Create a strategy design brief template covering hypothesis, data, risk, and execution assumptions.
- Build a dashboard tracking returns, drawdowns, turnover, and exposure concentration.
- Draft a pre-live deployment checklist for model, infrastructure, and risk controls.
