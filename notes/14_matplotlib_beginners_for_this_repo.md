# Matplotlib for this repository (beginner guide)

This note explains **Matplotlib** patterns used in this project: line charts of prices and equity, shaded regions for positions and drawdowns, histograms, and one **Seaborn** heatmap layered on a Matplotlib axes. It assumes you can load a pandas `DataFrame` with a datetime index; see `notes/13_pandas_beginners_for_this_repo.md`.

Companion material: `notes/10_pandas_numpy_matplotlib_beginner_guide.txt`, `notes/12_numpy_beginners_for_this_repo.md`.

---

## 1. Import convention

```python
import matplotlib.pyplot as plt
```

`pyplot` provides a stateful interface; in this repo you mostly use the **object-oriented** style: create a `Figure` and one or more `Axes`, then call methods on `ax` or `axes[i]`.

---

## 2. One axes: `fig, ax = plt.subplots(...)`

Single-panel plots appear in `src/binance_hist_candles.py`, `strategies/sma_crossover.py`, and parts of `backtesting/event_driven.py`:

```python
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df.index, df["close"], linewidth=0.8, color="steelblue", label="Close")
ax.set_title("BTC/USDT with Moving Averages")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

**Terms**

- **`fig`**: the whole window (canvas + metadata).
- **`ax`**: one plotting area (x-axis, y-axis, lines drawn on it).
- **`figsize=(width, height)`**: size in **inches** (not pixels).

---

## 3. Multiple stacked panels: `plt.subplots(nrows, ncols, ...)`

Strategies and the vectorised backtest stack **two** charts with shared time axis:

```python
fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
```

**Parameters used here**

- `(2, 1)`: two rows, one column → `axes[0]` (top), `axes[1]` (bottom).
- **`sharex=True`**: zoom/pan on the x-axis stays aligned between panels.
- **`gridspec_kw={"height_ratios": [2, 1]}`**: top panel gets twice the vertical space of the bottom (common for “price + indicator” layouts).

---

## 4. Line plots: `ax.plot(x, y, ...)`

**x** is usually the **DatetimeIndex** (`df.index`); **y** is a numeric column (`df["close"]`, `df["SMA_20"]`, equity series, etc.).

Common keyword arguments in this repo:

| Keyword | Role |
|--------|------|
| `linewidth` | Line thickness |
| `color` | Named colour or hex |
| `linestyle` | e.g. `"--"` for dashed reference lines |
| `label` | Text for the legend |
| `alpha` | Transparency (0 invisible, 1 opaque) |
| `zorder` | Draw order (higher on top) |

Multiple `plot` calls on the same `ax` overlay series (e.g. close plus two SMAs).

---

## 5. Markers for discrete events: `ax.scatter`

`sma_crossover.py` marks buy and sell points with triangles:

```python
ax.scatter(buy_signals.index, buy_signals["close"], marker="^", color="green", s=80, label="Buy", zorder=4)
```

**`s`** controls marker area (roughly “size”). Subset the DataFrame first so scatter receives only event rows.

---

## 6. Titles and axis labels

```python
ax.set_title("…")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USDT)")
```

When `sharex=True`, the bottom panel typically carries the x-axis label so it is not duplicated on every row.

---

## 7. Legends and grids

```python
ax.legend(loc="best")   # or loc="lower left", fontsize=8, etc.
ax.grid(True, alpha=0.3)
```

Every plotted series that should appear in the legend needs a **`label=`** on the `plot` / `scatter` / `fill_between` call (some `fill_between` calls omit labels if decorative).

---

## 8. Reference lines: `ax.axhline` and `ax.axvline`

Horizontal line at a constant y (e.g. zero momentum, equity baseline):

```python
ax.axhline(0, color="black", linestyle="--", linewidth=1)
axes[0].axhline(1, color="gray", linewidth=0.6, linestyle=":")
```

Vertical line at an x value (e.g. zero log return on a histogram):

```python
ax.axvline(0, color="black", linestyle="--", linewidth=1)
```

---

## 9. Filled regions: `ax.fill_between`

**Drawdown** (vectorised backtest): fill between 0 and negative drawdown in percent:

```python
axes[1].fill_between(res.index, 0, drawdown * 100, alpha=0.4, color=color, label=name)
```

**Position shading** (momentum): fill under price while long or short:

```python
axes[0].fill_between(long_positions.index, long_positions["close"], color="green", alpha=0.1, label="Long")
```

**Conditional fill** on the momentum line uses **`where=`** with a boolean mask aligned to the index:

```python
axes[1].fill_between(
    df_momentum.index,
    df_momentum["momentum"],
    where=df_momentum["momentum"] > 0,
    color="green",
    alpha=0.1,
    label="Positive Momentum",
)
```

The mask must have the **same length** as `x` (here the full index).

---

## 10. Histograms: `ax.hist`

`src/binance_hist_candles.py` plots the distribution of log returns:

```python
counts, bins, patches = ax.hist(log_returns, bins=50, density=False, alpha=0.7, color="steelblue", edgecolor="black")
```

A smooth curve is overlaid with `ax.plot(x, y, …)` on the same axes. Bin width for scaling a density curve is derived from `bins` (see that script for the full pattern).

---

## 11. Layout: `plt.tight_layout()`

Adjusts subplot padding so titles and labels overlap less. Call it before `plt.show()`.

---

## 12. Displaying figures: `plt.show()`

In scripts, **`plt.show()`** opens the interactive window and **blocks** until you close it (default behaviour).  

`backtesting/vectorised_backtest.py` temporarily replaces `plt.show` with a non-blocking version while importing strategy modules (so many figures can queue), then restores the real `plt.show` and may call `plt.show(block=False)`. For your own notebooks, a single `plt.show()` at the end of the cell is usually enough.

---

## 13. Heatmap with Seaborn (used in this repo)

`backtesting/event_driven.py` builds a pivot table of Sharpe ratios by `(fast, slow)` parameters, then:

```python
import seaborn as sns

pivot = grid_results.pivot(index="slow", columns="fast", values="sharpe")
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pivot, annot=False, fmt=".2f", cmap="RdYlGn", center=0, ax=ax, cbar_kws={"label": "Sharpe ratio"})
ax.set_title("Sharpe Ratio: SMA Crossover (fast vs slow)")
```

**Concept:** Seaborn draws into the **Matplotlib** `ax` you pass. You still set titles and labels on `ax`; colour scale is the heatmap’s **colorbar**.

---

## 14. Mental checklist

1. **Same length:** `plot` and `fill_between` x and y (or `where`) must align row-for-row with the index you pass.
2. **NaNs:** Matplotlib skips gaps; long leading NaNs from rolling windows can make lines start mid-sample—often you slice or `dropna` first.
3. **Many figures:** each `plt.subplots()` creates a new figure; close old windows or reuse one `fig` if memory becomes an issue.
4. **Scripts vs notebooks:** in Jupyter, figures often appear inline without blocking; in plain Python, you need `plt.show()` unless you save to file (`fig.savefig("out.png", dpi=150)`).

---

## 15. Optional practice

1. Reproduce a single-panel close-price chart for one calendar year using `df.loc["YYYY"]`.
2. Add a second line for `SMA_20` and a legend; match colours from `binance_hist_candles.py`.
3. On a second figure, plot cumulative strategy return and buy-and-hold from a backtest `DataFrame` using two `plot` calls and `axhline(1, …)`.

---

## 16. Official reference

The [Matplotlib documentation](https://matplotlib.org/stable/users/index.html) (User’s Guide and API) is the authoritative source. For Seaborn heatmaps, see the [Seaborn API](https://seaborn.pydata.org/generated/seaborn.heatmap.html).
