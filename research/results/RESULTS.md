# Out-of-sample results (2020-01-01 to 2026-10-09, 2474 days, costs 0.15% per side)

|                                      | Total return   | Annual return   | Volatility   |   Sharpe | Max drawdown   | Days in market   |   Trades per year | Sharpe minus B&H, 95% CI   |
|:-------------------------------------|:---------------|:----------------|:-------------|---------:|:---------------|:-----------------|------------------:|:---------------------------|
| Buy and hold BTC                     | +1046.8%       | +43.3%          | +61.1%       |     0.59 | -76.6%         |                  |                   |                            |
| MA crossover (walk-forward)          | +411.5%        | +27.2%          | +46.1%       |     0.52 | -53.6%         | 54%              |               7.5 | -0.59 to +0.52             |
| MA crossover (untuned 20/50)         | +798.6%        | +38.3%          | +41.9%       |     0.77 | -59.2%         | 56%              |               8.1 |                            |
| Momentum (walk-forward)              | +1128.4%       | +44.8%          | +41.6%       |     0.89 | -59.5%         | 56%              |              22.6 | -0.26 to +0.90             |
| Momentum (untuned 20)                | +774.7%        | +37.7%          | +40.8%       |     0.78 | -59.1%         | 55%              |              39.7 |                            |
| Mean reversion (walk-forward)        | -39.2%         | -7.1%           | +33.0%       |    -0.22 | -54.5%         | 13%              |              22.9 | -1.52 to -0.10             |
| Mean reversion (untuned 20/-1.0/0.0) | +50.8%         | +6.2%           | +38.0%       |     0.16 | -41.4%         | 22%              |              38.8 |                            |

## In-sample vs out-of-sample Sharpe of the chosen settings (mean across windows)

| strategy       |   train_sharpe |   test_sharpe |   rank_corr |
|:---------------|---------------:|--------------:|------------:|
| MA crossover   |           1.14 |          0.32 |       -0.12 |
| Mean reversion |           0.69 |          0.25 |       -0.04 |
| Momentum       |           1.11 |          0.61 |        0.1  |

## Cost sensitivity (out-of-sample Sharpe)

|                  |   0.00% per side |   0.15% per side |   0.30% per side |
|:-----------------|-----------------:|-----------------:|-----------------:|
| MA crossover     |             0.55 |             0.52 |             0.45 |
| Momentum         |             0.85 |             0.89 |             0.79 |
| Mean reversion   |             0.14 |            -0.22 |            -0.33 |
| Buy and hold BTC |             0.59 |             0.59 |             0.59 |
## Cross-check: event-driven simulator (trades one day later), same positions

| Strategy | Vectorised Sharpe | Event-driven Sharpe | Event-driven total return |
|---|---|---|---|
| MA crossover | 0.52 | 0.38 | +234.0% |
| Momentum | 0.89 | 0.97 | +1480.1% |
| Mean reversion | -0.22 | -0.26 | -43.3% |
