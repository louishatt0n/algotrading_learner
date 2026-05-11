# NumPy

## Key Terms

- **Array**: Efficient typed numerical container.
- **Broadcasting**: Applying operations across arrays of compatible shapes.
- **Numerical stability**: Avoiding unreliable math behavior.

## What It Is

NumPy is a numerical computing library for fast array operations.

## Why It Is Used

This project uses NumPy for:

- Logarithms and exponentials (`np.log`, `np.exp`).
- Conditional vectorized signals (`np.where`).
- Square-root scaling for annualization (`np.sqrt`).

## Useful Commands

```python
import numpy as np
np.log(1.05)
np.exp(0.1)
np.sqrt(252)
np.where(condition, value_if_true, value_if_false)
```

## Useful Commands With Examples

```python
df["signal"] = np.where(
    df["z_score"] < -1.0,
    1,
    np.where(df["z_score"] > 0, -1, 0),
)

df["cumret"] = df["log_return"].cumsum().apply(np.exp)
```

## Advanced

### Deeper Concepts
- NumPy performance comes from vectorized operations and contiguous memory; understanding array shape and broadcasting is foundational.
- Differentiate element-wise operations from matrix operations and control dimensionality explicitly to avoid silent logic errors.
- Use dtype intentionally: numerical precision and memory usage materially affect scientific and trading computations.
- Move from loops to array expressions while preserving readability through clear intermediate naming and shape checks.

### Free Platforms and Courses
- [NumPy documentation](https://numpy.org/doc/) for the canonical guide to arrays, broadcasting, and linear algebra utilities.
- [Python docs](https://docs.python.org/3/) for core language reference when writing efficient numerical utilities.
- [MIT OCW Analytics of Finance](https://ocw.mit.edu/courses/15-450-analytics-of-finance-fall-2010/) for mathematically grounded applications.
- [freeCodeCamp algorithmic trading course](https://www.freecodecamp.org/news/algorithmic-trading-using-python-course/) for practical integration in strategy research.

### Practice Path
- Rewrite loop-based calculations as vectorized NumPy expressions and benchmark timing improvements.
- Practice broadcasting intentionally with shape annotations in markdown comments or notebook cells.
- Build a small library of reusable numerical utilities and unit-test edge cases (empty arrays, NaN, dtype conversion).
- Validate numerical outputs against hand-calculated examples for at least three operations.

### Suggested Mini-Projects
- Implement a vectorized return and volatility calculator for a basket of assets.
- Build a matrix-based scenario analysis tool for simple portfolio shocks.
- Create a benchmark notebook comparing pure Python loops vs NumPy implementations on realistic data sizes.
