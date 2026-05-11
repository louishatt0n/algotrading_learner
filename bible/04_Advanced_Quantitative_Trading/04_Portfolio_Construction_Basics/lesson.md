# Portfolio Construction Basics

## Key Terms

- **Allocation**: Capital split among strategies.
- **Correlation**: Degree of co-movement between return streams.

## Core Explanation

Combining multiple strategies can improve stability if return streams are not perfectly correlated.

Basic construction steps:

1. Collect strategy return series.
2. Inspect pairwise correlation.
3. Assign initial weights.
4. Rebalance periodically.

## Worked Example

Combine SMA, momentum, and mean reversion with equal weights; compare drawdown against each standalone strategy.

## Advanced

### Deeper Concepts
- Portfolio construction converts signals into allocations under constraints: turnover, exposure, liquidity, and risk budgets.
- Diversification should be evaluated using effective exposure and correlation structure, not just number of assets.
- Rebalancing frequency materially affects cost and risk, so it must be optimized jointly with signal design.
- Constraint handling should be explicit and auditable for production readiness.

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
- Build a constrained allocation routine with exposure and turnover limits.
- Compare equal-weight, risk-parity, and signal-weighted allocations on the same dataset.
- Produce a portfolio diagnostics notebook focused on diversification and concentration risk.
