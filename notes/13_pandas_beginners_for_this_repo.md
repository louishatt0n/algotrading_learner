# pandas for this repository (beginner guide)

This note explains **pandas** skills used throughout this project: loading OHLC data, building indicators, aligning signals in time, cleaning rows, and summarising backtest results. It assumes basic Python; it does not assume prior data-science experience.

Companion material:

- `notes/10_pandas_numpy_matplotlib_beginner_guide.txt` — broader walkthrough, including Binance API → DataFrame patterns.
- `notes/12_numpy_beginners_for_this_repo.md` — NumPy functions applied to columns (`np.log`, `np.where`, etc.).

---

## 1. What a DataFrame is

A **DataFrame** is a table: named **columns** (for example `open`, `high`, `low`, `close`, `volume`) and **rows** (one observation per timestamp). The **index** labels rows; in this repo the index is usually a **DatetimeIndex** built from the `date` column or from `open_time` after loading API data.

Think of each column as a **time-aligned series** of numbers or labels. Operations between two columns align by **row index**, not by position in memory.

---

## 2. Import and CSV loading

Convention:

```python
import pandas as pd
```

The canonical load for bundled daily data (`src/data_loader.py`):

```python
df = pd.read_csv("data/btc_daily.csv", index_col="date", parse_dates=True)
```

**Parameters to understand**

- `index_col="date"`: use the `date` column as the row index instead of leaving default `0, 1, 2, …`.
- `parse_dates=True`: convert that column to datetime objects so you can slice by date and use time-based logic.

After loading, `df["close"]` is the series of closing prices indexed by date.

---

## 3. Reading and writing columns

**Read** a column:

```python
df["close"]
```

**Create or overwrite** a column (right-hand side is computed per row):

```python
df["log_return"] = np.log(df["close"] / df["close"].shift(1))
```

Use **bracket** notation `df["name"]` for arbitrary column names (including names with spaces or dynamic names like `f"SMA_{fast}"`). Dot access (`df.close`) only works for simple identifiers and is easier to confuse with methods; this repo consistently uses brackets.

---

## 4. `df.copy()` before mutating

Strategy functions start with:

```python
df = df.copy()
```

**Why:** Passing a DataFrame into a function can share the same underlying object with the caller. Assigning new columns without copying can accidentally modify the caller’s data. Copying makes the function’s edits **local** and predictable.

---

## 5. `shift`: lag values and avoid look-ahead

`shift(k)` moves a series **down** by `k` rows: row `t` sees the value that originally belonged to `t - k`.

- `df["close"].shift(1)` is the **previous** bar’s close (used for daily log returns).
- `df["close"].shift(window)` is the close from **window** bars ago (used in momentum).
- `df["signal"].shift(1)` delays the trading signal by one bar so **position** applies from the next period (reduces accidental use of same-bar information in backtests).

Leading rows where history does not exist become **`NaN`**.

---

## 6. `rolling`: moving windows

**Rolling** statistics compute a value over a trailing window of fixed length.

Examples from this repo:

```python
df[f"SMA_{fast}"] = df["close"].rolling(window=fast).mean()
df[f"SMA_{slow}"] = df["close"].rolling(window=slow).mean()
```

Mean reversion uses rolling mean and standard deviation:

```python
df["rolling_mean"] = df["close"].rolling(window=window).mean()
df["rolling_std"] = df["close"].rolling(window=window).std()
```

The first `window - 1` rows typically have **`NaN`** for those columns because the window is incomplete. Backtests and plots usually **drop** those rows before computing metrics, or rely on `dropna` on the columns you need.

---

## 7. `dropna` and `subset`

`dropna()` removes rows with missing values. Restricting which columns matter avoids dropping valid rows unnecessarily.

Vectorised backtest (`backtesting/vectorised_backtest.py`):

```python
result = ohlc.copy().dropna(subset=["position", "log_return"])
```

Event-driven path (`backtesting/event_driven.py`):

```python
data = df_strategy.dropna(subset=["position"]).copy()
```

**Interpretation:** if either `position` or `log_return` is missing, that row cannot participate in the return calculation; drop it.

---

## 8. Positional vs label indexing: `iloc` and `loc`

- **`iloc`**: select by **integer position** (`0` = first row, `-1` = last row).  
  Example: `equity_df["equity"].iloc[-1]` for final equity.

- **`loc`**: select by **index label**, including **slices** on a DatetimeIndex.  
  Examples from `src/binance_hist_candles.py`:

```python
df_2024 = df.loc["2024"]
df_on_2024_06_15 = df.loc["2024-06-15"]
```

Walk-forward code uses **label slices** on OHLC (`backtesting/event_driven.py`):

```python
df_train = ohlc.loc[window_start:train_end]
df_test = ohlc.loc[train_end:test_end]
```

End points are **inclusive** on both sides for `loc` slice notation on ordered indices (be mindful of duplicates in the index; daily data here is usually unique per date).

---

## 9. Building a DataFrame from raw rows

When an API returns a list of rows (`src/binance_hist_candles.py`):

```python
df = pd.DataFrame(klines, columns=columns)
```

The **order** and **count** of `columns` must match each row in `klines`. Then convert types and parse times:

```python
df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
df[col] = df[col].astype(float)
df.set_index("open_time", inplace=True)
```

`unit="ms"` means integers are **milliseconds since the Unix epoch**.

---

## 10. `pct_change`, `std`, `mean`, `cummax`

**Percentage change** (simple returns) between consecutive values:

```python
daily_returns = equity_df["equity"].pct_change().dropna()
```

Used with `mean()` and `std()` for Sharpe-style ratios in `event_driven.py`.

**Cumulative maximum** of equity for drawdown:

```python
rolling_max = equity_df["equity"].cummax()
max_drawdown = ((equity_df["equity"] - rolling_max) / rolling_max).min()
```

`cummax` is **expanding**: at each date it stores the highest equity seen up to that date.

---

## 11. Aggregating results: `DataFrame` from records, `sort_values`

Grid search accumulates Python dictionaries, then wraps them:

```python
return pd.DataFrame(results).sort_values(by="sharpe", ascending=False)
```

**Pattern:** `results` is a list of dicts with identical keys (`fast`, `slow`, `sharpe`, …). `pd.DataFrame(results)` builds one row per dict. `sort_values` orders rows for inspection of the best parameter sets.

---

## 12. `set_index` and reconstructing series from lists

Equity curves are often list-of-dicts with a `date` field:

```python
equity_df = pd.DataFrame(portfolio.equity_curve).set_index("date")
```

`set_index` promotes `date` to the index so plotting and time alignment behave like OHLC data.

---

## 13. Iterating rows: `iterrows` (use sparingly)

Event-driven simulation loops:

```python
for date, row in data.iterrows():
    price = row["close"]
    position = row["position"]
```

**Trade-off:** `iterrows` is **slow** compared to vectorised code, but it is **clear** when each day triggers buy/sell logic with state (cash, position, portfolio object). For whole-column math, prefer vectorised operations and avoid Python-level loops.

---

## 14. Date arithmetic: `pd.DateOffset`

Walk-forward windows advance with:

```python
train_end = window_start + pd.DateOffset(months=train_months)
test_end = train_end + pd.DateOffset(months=test_months)
window_start += pd.DateOffset(months=test_months)
```

This keeps calendar-based train/test boundaries consistent when slicing with `loc`.

---

## 15. Mental checklist when editing strategy tables

1. **Index:** Is the frame sorted by time? Duplicate timestamps break `loc` slices and shifts.
2. **Copy:** Does the function call `df = df.copy()` before assigning columns?
3. **NaNs:** Do rolling and `shift` leave a warm-up region? Drop or handle explicitly.
4. **Alignment:** Every binary column operation aligns on **index**; merging two frames requires compatible indexes unless you use join/merge deliberately.
5. **Execution lag:** Signals vs `position = signal.shift(1)` — changing one without the other changes economic meaning.

---

## 16. Optional practice

1. Load `data/btc_daily.csv` with `index_col` and `parse_dates`, print `df.head()`, `df.tail()`, and `df.info()`.
2. Recompute `SMA_20` and `SMA_50` with `rolling`, then plot `close` and both SMAs for one calendar year using `loc["2023":"2023"]` (adjust year to your file range).
3. Build a tiny `DataFrame` from three dict rows and sort it by a numeric column descending.

---

## 17. Official reference

The [pandas documentation](https://pandas.pydata.org/docs/) contains the User Guide and the API reference for every method named above. Use it as the authoritative source when this note’s scope ends.
