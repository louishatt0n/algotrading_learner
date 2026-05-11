# Matplotlib

## Key Terms

- **Figure**: Entire drawing canvas.
- **Axes**: Plot area with scales and labels.
- **Subplot**: Multiple plot areas in one figure.

## What It Is

Matplotlib is a plotting library for static visualizations in Python.

## Why It Is Used

In this project, Matplotlib is used to visualize:

- Price series and moving averages.
- Strategy markers and signals.
- Equity curves and drawdowns.
- Distribution and diagnostic plots.

## Useful Commands

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df.index, df["close"])
ax.set_title("BTC/USDT")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## Useful Commands With Examples

```python
fig, axes = plt.subplots(2, 1, figsize=(14, 8), sharex=True)
axes[0].plot(df.index, df["close"], color="steelblue")
axes[1].plot(df.index, df["momentum"], color="purple")
axes[1].axhline(0, linestyle="--", color="black")
```

```python
ax.scatter(buy_points.index, buy_points["close"], marker="^", color="green")
ax.scatter(sell_points.index, sell_points["close"], marker="v", color="red")
```

## Advanced

### Deeper Concepts
- Plotting is analytical communication: chart type, scale, and annotation choices should match the question being answered.
- Understand figure and axes objects directly rather than relying only on implicit state; this yields clearer, maintainable plotting code.
- Design for interpretability by controlling labels, legends, color palettes, and reference lines with intentional consistency.
- Treat visual diagnostics as part of model and strategy validation, not decorative output.

### Free Platforms and Courses
- [Matplotlib user guide](https://matplotlib.org/stable/users/index.html) for complete plotting concepts and API usage.
- [Python docs](https://docs.python.org/3/) for language features helpful in reusable plotting utilities.
- [Jupyter documentation](https://docs.jupyter.org/en/stable/) for notebook-centric visualization workflows.
- [Khan Academy finance](https://www.khanacademy.org/economics-finance-domain/core-finance) for economic context to shape meaningful visual narratives.

### Practice Path
- Recreate the same data story using line, bar, and scatter charts; compare what each reveals or hides.
- Build one reusable plotting function with arguments for titles, labels, style, and output path.
- Add annotations for major events and verify whether interpretation improves.
- Audit each plot with a quality checklist: readability, scale appropriateness, and non-misleading visual encoding.

### Suggested Mini-Projects
- Produce a mini dashboard of three coordinated charts describing trend, dispersion, and drawdown behavior.
- Create publication-ready figures exported in both notebook and script environments.
- Build a visual report template for evaluating strategy performance across different parameter settings.
