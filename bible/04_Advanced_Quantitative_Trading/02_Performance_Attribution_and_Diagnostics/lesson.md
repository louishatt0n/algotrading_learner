# Performance Attribution and Diagnostics

## Key Terms

- **Attribution**: Explaining where returns come from.
- **Exposure**: Fraction of time strategy is in market.
- **Hit rate**: Fraction of positive periods/trades.

## Core Explanation

Intermediate review asks:

- Which periods drove returns?
- Did gains come from few outliers?
- How much risk was taken for each gain?

Add rolling metrics and period-by-period summaries.

## Worked Example

Use rolling 60-day Sharpe and rolling drawdown to inspect stability across time, not only total-period outcome.

## Advanced

### Deeper Concepts
- Attribution explains why performance occurred: separate alpha, beta, timing, and cost effects.
- Diagnostics should include temporal stability, regime sensitivity, and exposure drift.
- Use benchmark-relative and absolute metrics jointly to avoid misleading conclusions.
- A diagnostic framework is only useful when linked to explicit strategy improvement decisions.

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
- Build a return decomposition report with factor and cost attribution.
- Create rolling diagnostics for Sharpe, hit rate, and drawdown behavior.
- Design a post-mortem template for underperforming periods.
