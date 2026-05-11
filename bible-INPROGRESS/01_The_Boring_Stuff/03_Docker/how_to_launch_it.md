# Docker: How To Launch It

## Core Explanation

Typical Docker flow:

1. Write `Dockerfile`.
2. Build image.
3. Run container.
4. Check logs.
5. Stop/remove container when finished.

## Worked Example

You can containerize a script runner that executes `python backtesting/vectorised_backtest.py`.
