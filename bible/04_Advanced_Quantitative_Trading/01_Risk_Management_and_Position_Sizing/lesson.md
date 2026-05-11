# Risk Management and Position Sizing

## Key Terms

- **Position sizing**: Choosing trade size as fraction of capital.
- **Volatility targeting**: Reducing size when volatility rises.
- **Kelly fraction**: Growth-optimal fraction under assumptions.

## Core Explanation

Good strategies can fail from poor sizing.  
Intermediate sizing methods include:

- Fixed fractional (e.g., 1% risk model).
- Volatility-adjusted size.
- Fractional Kelly (e.g., half-Kelly for stability).

## Worked Example

`event_driven.py` includes Kelly-style sizing logic (`run_backtest_kelly`) as a progression beyond all-in entries.

## Advanced

### Deeper Concepts
- Risk budgeting determines survival: position sizing frameworks should reflect volatility, correlation, and drawdown constraints.
- Leverage policy is a portfolio-level decision and should be scenario-tested under adverse regimes.
- Tail-risk awareness requires stress testing beyond normal-distribution assumptions.
- Risk controls should be pre-committed and mechanically enforceable to reduce discretionary drift.

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
- Implement volatility targeting and compare with fixed-notional sizing.
- Run stress scenarios and produce a risk budget allocation report.
- Build a drawdown-based de-risking overlay and evaluate trade-offs.
