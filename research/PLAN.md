# Walk-forward test plan (written before running the evaluation, 10 Oct 2026)

**Question:** do the three strategies in this repo (moving-average crossover, momentum, z-score mean
reversion) beat simply buying and holding Bitcoin once their settings are chosen without seeing the
data they are tested on, and after trading costs?

## Data
- Daily BTC/USDT candles from Binance, 17 Aug 2017 to 9 Oct 2026 (`src/fetch_binance_daily.py`).
- Signals at day *t* use closes up to *t−1* only (each strategy shifts its signal by one day).

## Design (fixed in advance)
- **Walk-forward, rolling window:** tune on the previous 24 months, trade the next 6 months, then roll
  forward 6 months. Test windows run from 1 Jan 2020 to 9 Oct 2026 (14 windows, the last one partial).
- **Tuning rule:** in each training window pick the parameters with the highest Sharpe ratio after costs.
- **Parameter grids:**
  - Moving-average crossover: fast ∈ {5, 10, 20, 30, 50}, slow ∈ {50, 100, 150, 200}, fast < slow (19 settings)
  - Momentum: lookback ∈ {5, 10, 20, 30, 60, 90, 120, 180} days (8 settings)
  - Mean reversion: window ∈ {10, 20, 30, 60}, entry z ∈ {−0.5, −1, −1.5, −2}, exit z ∈ {0, 0.5, 1} (48 settings)
- **Long or flat only:** sell signals mean "hold cash", because shorting spot Bitcoin needs derivatives
  with funding costs this project does not model.
- **Costs:** 0.15% per side (0.10% commission + 0.05% slippage, the defaults in `event_driven.py`),
  charged on every change of position, including at window boundaries.
- **Benchmark:** buy and hold Bitcoin over exactly the same out-of-sample dates.
- **Also reported:** the original untuned settings (20/50, 20-day, 20/−1) as fixed baselines; cost
  sensitivity at 0% and 0.30% per side; the gap between in-sample and out-of-sample Sharpe; and a
  block-bootstrap 95% confidence interval (20-day blocks, 5,000 resamples) for each strategy's Sharpe
  minus buy-and-hold's.

## Metrics
Annualised with 365 days: total return, annual return (CAGR), volatility, Sharpe ratio (risk-free rate 0),
maximum drawdown, share of days in the market, trades per year, and total cost drag.

## Cross-check
Re-run the walk-forward moving-average strategy through the event-driven `Portfolio` simulator and confirm
the two backtesters agree.
