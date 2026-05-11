# NumPy for this repository (beginner guide)

This note explains the **NumPy** ideas you need to read and extend the trading code in this project. It assumes you can run Python and open a `.py` file; it does not assume prior array programming.

For pandas and plotting alongside this material, see `notes/10_pandas_numpy_matplotlib_beginner_guide.txt` and `notes/11-jupyter_notebook_beginners_guide.md`.

---

## 1. Why NumPy appears here

In this repository, market data live mainly in **pandas** `DataFrame` objects (tables with columns such as `close`). Many columns behave like **sequences of numbers** (one value per row). NumPy provides **element-wise** mathematical functions that operate on those sequences efficiently:

- `np.log`, `np.exp`, `np.sqrt` applied to a column return a column of the same length, with the function evaluated **per row**.
- `np.where` builds **signals** (long / short / flat) from conditions on price or indicators.

You rarely construct raw `np.ndarray` objects by hand in the strategies; instead you combine **pandas** (rolling means, shifts) with **NumPy** (math and branching).

---

## 2. Import convention

Every file in this repo that uses NumPy follows the usual alias:

```python
import numpy as np
```

Always use the `np.` prefix so it is obvious which functions are NumPy (for example `np.log`, not `log`).

---

## 3. Log returns: `np.log`

**Log return** between consecutive closes is defined as:

\[
\log\left(\frac{\text{close}_t}{\text{close}_{t-1}}\right)
\]

In code (see `src/data_loader.py`, `backtesting/vectorised_backtest.py`):

```python
df["log_return"] = np.log(df["close"] / df["close"].shift(1))
```

**What to understand**

- `df["close"].shift(1)` is yesterday’s close (pandas).
- The ratio `close / close.shift(1)` is **element-wise**: each row uses that row’s close divided by the **previous** row’s close.
- `np.log` applies the natural logarithm to **each** ratio. The first row(s) may be invalid until a prior close exists; pandas often produces `NaN` there, which later code drops with `dropna`.

**Momentum** uses the same idea over a longer window (see `strategies/momentum.py`):

```python
df["momentum"] = np.log(df["close"] / df["close"].shift(window))
```

---

## 4. Cumulative returns: `np.exp` with `cumsum`

If \(r^{(log)}_t\) is the log return on day \(t\), the **cumulative** multiplicative return through time uses the identity:

\[
\text{cumulative growth factor} = \exp\left(\sum_t r^{(log)}_t\right)
\]

In this project, log returns are summed with pandas `cumsum`, then `np.exp` is applied per element (see `backtesting/vectorised_backtest.py`):

```python
result["cumret_strategy"] = result["strategy_return"].cumsum().apply(np.exp)
result["cumret_buyandhold"] = result["log_return"].cumsum().apply(np.exp)
```

**What to understand**

- `cumsum()` builds running sums of log returns.
- `.apply(np.exp)` exponentiates **each** running sum, producing a **wealth index** style series (starting near 1 if the first sums are near zero).
- Strategy returns are log returns **scaled by position** (`strategy_return = log_return * position`) before the same cumulative recipe.

---

## 5. Annualised volatility: `np.sqrt`

Trading code often **annualises** daily standard deviation by scaling by \(\sqrt{252}\), where 252 is a conventional number of **trading days** per year (see `backtesting/vectorised_backtest.py`):

```python
annual_vol = result["strategy_return"].std() * np.sqrt(252)
```

**What to understand**

- If daily returns are independent and identically distributed with variance \(\sigma^2_{\text{daily}}\), a common scaling rule treats annual variance as \(252 \,\sigma^2_{\text{daily}}\), hence annual volatility \(\sigma_{\text{annual}} \approx \sqrt{252}\,\sigma_{\text{daily}}\).
- This is a **modeling convention**, not a law of nature; it is standard in equity-style backtests.

---

## 6. Branching signals: `np.where`

`np.where(condition, value_if_true, value_if_false)` chooses, **for each row**, which value to place in the new series. Conditions are compared **element-wise** to the column.

**Binary signal** (example pattern from `strategies/strategies.py`):

```python
df["signal"] = np.where(df[f"SMA_{fast}"] > df[f"SMA_{slow}"], 1, 0)
```

**Ternary signal** (three outcomes: long, short, flat) uses **nested** `np.where`, as in `strategies/mean_reversion.py`:

```python
df["signal"] = np.where(
    df["z_score"] < threshold,
    1,
    np.where(df["z_score"] > exit_z, -1, 0),
)
```

Read this as:

1. If `z_score < threshold`, signal is `1` (long).
2. Else, if `z_score > exit_z`, signal is `-1` (short).
3. Else signal is `0` (flat).

**What to watch**

- Conditions must align with the same index as the columns (they do when all terms are columns from the same `DataFrame`).
- Compare thresholds (`threshold`, `exit_z`) to **rolling** statistics carefully: early rows may be `NaN` until the window fills; signals there are unreliable until you `dropna` or shift positions for execution lag (this repo uses `position = signal.shift(1)` in strategies).

---

## 7. Sentinels and optimisation: `np.inf`

In `backtesting/event_driven.py`, search loops initialise “best so far” with negative infinity so any real Sharpe ratio beats it:

```python
best_sharpe = -np.inf
```

**What to understand**

- `np.inf` and `-np.inf` are floating-point infinities; they compare predictably (`3.0 > -np.inf` is true).
- Use them only as **internal bookkeeping**, not as financial outputs.

---

## 8. Density plots and grids: `np.linspace`, `np.pi`, `np.exp`

`src/binance_hist_candles.py` builds a grid of x-values and evaluates a Gaussian density for comparison with a histogram of log returns:

```python
x = np.linspace(log_returns.min(), log_returns.max(), 300)
normal_pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
```

**What to understand**

- `np.linspace(a, b, n)` returns `n` evenly spaced points from `a` to `b` (inclusive). Useful for plotting smooth curves.
- `np.pi` is the mathematical constant \(\pi\).
- Here `np.exp` is used inside the normal PDF formula, not for cumulative returns.

---

## 9. How pandas and NumPy interact

When you write `np.log(df["close"])`, pandas passes the underlying **array-like** data to NumPy and returns a **Series** with the same index. You do not need to call `.values` for these patterns.

If you ever need an explicit NumPy array (for example for a third-party function), `df["close"].to_numpy()` is the modern spelling; use it only when something **requires** a raw array.

---

## 10. Mental checklist before you change strategy math

1. **Shapes and index**: Every binary operation between two columns should be row-aligned (same `DataFrame`, same length).
2. **NaNs**: Rolling windows and shifts create leading `NaN`s; backtests usually `dropna(subset=[...])` before metrics.
3. **Look-ahead**: Signals are often shifted (`shift(1)`) so positions apply from the **next** bar; NumPy does not enforce this—**you** must keep timing consistent.
4. **Interpretation**: `np.where` encodes discrete rules; small changes to thresholds reorder many rows—test on a short date range first.

---

## 11. Minimal practice exercises (optional)

1. Recompute `log_return` for a small CSV and verify by hand on three rows that `np.log(close_t / close_{t-1})` matches your spreadsheet.
2. Rebuild a nested `np.where` that encodes: long if close > 20-day SMA, else short if close < 50-day SMA, else 0. Compare to `strategies/sma_crossover.py`.
3. Given a dummy daily return series, compute `std() * np.sqrt(252)` and confirm increasing the series length changes `std` slightly (sampling noise).

---

## 12. Official reference

For definitions of every function mentioned here, use the [NumPy documentation](https://numpy.org/doc/stable/reference/index.html) (user guide and API reference). Treat it as the authoritative supplement when this note’s scope ends.
