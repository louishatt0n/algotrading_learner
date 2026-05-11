# Git: Commands And Examples

## Commands

```bash
git status
git add .
git commit -m "Describe change clearly"
git pull --rebase origin main
git push origin main
```

## Worked Example

```bash
git checkout -b feature/new-backtest-metric
python backtesting/event_driven.py
git add backtesting/event_driven.py
git commit -m "Add walk-forward reporting fix"
```
