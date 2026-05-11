# Regime Detection and Filtering

## Key Terms

- **Regime**: Market condition state (trend, range, high vol, low vol).
- **Filter**: Rule deciding whether strategy is active.

## Core Explanation

A strategy often works only in certain conditions.  
Regime filtering activates strategy only when matching conditions are present.

Example filters:

- Trend filter (price above long SMA).
- Volatility filter (realized vol in acceptable band).

## Worked Example

Apply mean reversion only when trend strength is weak, and momentum only when trend strength is strong.

## Advanced

### Deeper Concepts
- Regime detection attempts to condition strategy behavior on changing market states such as volatility, trend, and correlation structure.
- Classification models should prioritize interpretability and stability over complexity.
- Filtering rules can reduce drawdowns but may also cut upside; evaluate net benefit with realistic costs.
- Regime boundaries are uncertain, so confidence-aware decision rules are preferable.

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
- Implement a simple regime classifier and compare strategy performance with/without filtering.
- Measure false-positive and false-negative regime classification impacts.
- Create a regime-aware position sizing overlay with documented decision logic.
