"""Walk-forward, out-of-sample evaluation of the three strategies (design fixed in research/PLAN.md).

For each 6-month test window from 2020 onwards:
  1. score every parameter setting on the previous 24 months (Sharpe after costs),
  2. trade the best setting on the next 6 months, which it has never seen,
  3. stitch the test windows together into one out-of-sample track record.

Run from the project root:  python research/walk_forward_eval.py
Outputs go to research/results/.
"""
import sys
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.data_loader import load_prices, PERIODS_PER_YEAR
from strategies.sma_crossover import sma_crossover
from strategies.momentum import momentum_strategy
from strategies.mean_reversion import mean_reversion_strategy

OUT = ROOT / "research" / "results"
COST = 0.0015                      # per side: 0.10% commission + 0.05% slippage
TRAIN_MONTHS, TEST_MONTHS = 24, 6
FIRST_TEST = pd.Timestamp("2020-01-01")
RNG = np.random.default_rng(20261010)

GRIDS = {
    "MA crossover": [dict(fast=f, slow=s) for f, s in product([5, 10, 20, 30, 50], [50, 100, 150, 200]) if f < s],
    "Momentum": [dict(window=w) for w in [5, 10, 20, 30, 60, 90, 120, 180]],
    "Mean reversion": [dict(window=w, threshold=t, exit_z=e)
                       for w, t, e in product([10, 20, 30, 60], [-0.5, -1.0, -1.5, -2.0], [0.0, 0.5, 1.0])],
}
BUILD = {"MA crossover": sma_crossover, "Momentum": momentum_strategy, "Mean reversion": mean_reversion_strategy}
UNTUNED = {"MA crossover": dict(fast=20, slow=50), "Momentum": dict(window=20),
           "Mean reversion": dict(window=20, threshold=-1.0, exit_z=0.0)}


def long_flat_position(px, name, params):
    """Position (1 = long, 0 = cash) for each day, from the repo's own strategy functions."""
    pos = BUILD[name](px, **params)["position"]
    return pos.clip(lower=0).fillna(0)          # sell signal -> hold cash (no shorting spot BTC)


def net_log_returns(pos, logret, cost):
    """Daily log return after costs; cost charged on every change of position."""
    turnover = pos.diff().abs().fillna(pos.abs())
    return pos * logret + np.log(1 - turnover * cost)


def sharpe(r):
    sd = r.std()
    return r.mean() / sd * np.sqrt(PERIODS_PER_YEAR) if sd > 0 else 0.0


def metrics(r, pos=None):
    eq = np.exp(r.cumsum())
    years = len(r) / PERIODS_PER_YEAR
    out = {
        "Total return": eq.iloc[-1] - 1,
        "Annual return": eq.iloc[-1] ** (1 / years) - 1,
        "Volatility": r.std() * np.sqrt(PERIODS_PER_YEAR),
        "Sharpe": sharpe(r),
        "Max drawdown": (eq / eq.cummax() - 1).min(),
    }
    if pos is not None:
        out["Days in market"] = pos.mean()
        out["Trades per year"] = (pos.diff().abs().fillna(pos.abs()) > 0).sum() / years
    return out


def windows(index):
    """(train_start, train_end, test_start, test_end) for each 6-month test window."""
    out, ts = [], FIRST_TEST
    while ts <= index[-1]:
        te = min(ts + pd.DateOffset(months=TEST_MONTHS) - pd.Timedelta(days=1), index[-1])
        tr_s = ts - pd.DateOffset(months=TRAIN_MONTHS)
        out.append((tr_s, ts - pd.Timedelta(days=1), ts, te))
        ts += pd.DateOffset(months=TEST_MONTHS)
    return out


def walk_forward(px, name, cost):
    logret = px["log_return"]
    # Each setting's position depends only on past prices, so it can be computed once on the full history
    positions = {i: long_flat_position(px, name, p) for i, p in enumerate(GRIDS[name])}
    nets = {i: net_log_returns(pos, logret, cost) for i, pos in positions.items()}
    stitched, rows = [], []
    for tr_s, tr_e, ts, te in windows(px.index):
        train = {i: sharpe(n.loc[tr_s:tr_e]) for i, n in nets.items()}
        best = max(train, key=train.get)
        test = {i: sharpe(n.loc[ts:te]) for i, n in nets.items()}
        rank_corr = pd.Series(train).rank().corr(pd.Series(test).rank())  # do in-sample winners stay winners?
        stitched.append(positions[best].loc[ts:te])
        rows.append({"test_start": ts.date(), "test_end": te.date(), "chosen": GRIDS[name][best],
                     "train_sharpe": train[best], "test_sharpe": test[best], "rank_corr": rank_corr})
    pos = pd.concat(stitched)
    r = net_log_returns(pos, logret.loc[pos.index], cost)   # recompute so boundary switches pay costs too
    return pos, r, pd.DataFrame(rows)


def block_bootstrap_sharpe_diff(r_a, r_b, block=20, reps=5000):
    """95% CI for Sharpe(a) - Sharpe(b), resampling paired days in 20-day blocks (keeps autocorrelation)."""
    a, b = r_a.values, r_b.values
    n = len(a); k = int(np.ceil(n / block))
    starts = RNG.integers(0, n - block + 1, size=(reps, k))
    idx = (starts[:, :, None] + np.arange(block)).reshape(reps, -1)[:, :n]
    A, Bm = a[idx], b[idx]
    s = lambda X: X.mean(1) / X.std(1, ddof=1) * np.sqrt(PERIODS_PER_YEAR)
    d = s(A) - s(Bm)
    return np.percentile(d, [2.5, 97.5])


def fmt(m):
    pct = lambda v: f"{v:+.1%}" if v == v else ""
    return {k: (f"{v:.2f}" if k == "Sharpe" else f"{v:.1f}" if k == "Trades per year" else pct(v) if k != "Days in market" else f"{v:.0%}")
            for k, v in m.items()}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    px = load_prices()
    first, last = FIRST_TEST, px.index[-1]
    bh = px["log_return"].loc[first:last]
    bh_net = bh.copy(); bh_net.iloc[0] += np.log(1 - COST)            # buy once, never sell
    rows, curves, wins_all = {"Buy and hold BTC": metrics(bh_net)}, {"Buy and hold BTC": bh_net}, []
    ci = {}
    for name in GRIDS:
        pos, r, w = walk_forward(px, name, COST)
        rows[f"{name} (walk-forward)"] = metrics(r, pos)
        curves[f"{name} (walk-forward)"] = r
        ci[f"{name} (walk-forward)"] = block_bootstrap_sharpe_diff(r, bh_net.loc[r.index])
        w.insert(0, "strategy", name); wins_all.append(w)
        upos = long_flat_position(px, name, UNTUNED[name]).loc[first:last]
        ur = net_log_returns(upos, px["log_return"].loc[first:last], COST)
        rows[f"{name} (untuned {'/'.join(str(v) for v in UNTUNED[name].values())})"] = metrics(ur, upos)
    table = pd.DataFrame(rows).T
    table["Sharpe minus B&H, 95% CI"] = [f"{ci[i][0]:+.2f} to {ci[i][1]:+.2f}" if i in ci else "" for i in table.index]
    wins = pd.concat(wins_all)

    # cost sensitivity for the walk-forward versions
    sens = {}
    for c in [0.0, COST, 0.003]:
        sens[f"{c:.2%} per side"] = {name: walk_forward(px, name, c)[1].pipe(sharpe) for name in GRIDS}
    sens = pd.DataFrame(sens)
    sens.loc["Buy and hold BTC"] = sharpe(bh_net)

    gap = wins.groupby("strategy")[["train_sharpe", "test_sharpe", "rank_corr"]].mean()

    table.to_csv(OUT / "summary.csv"); wins.to_csv(OUT / "windows.csv", index=False)
    sens.to_csv(OUT / "cost_sensitivity.csv"); gap.to_csv(OUT / "in_vs_out_of_sample.csv")

    shown = pd.DataFrame({k: fmt(v) for k, v in rows.items()}).T
    shown["Sharpe minus B&H, 95% CI"] = table["Sharpe minus B&H, 95% CI"]
    lines = [f"# Out-of-sample results ({first.date()} to {last.date()}, {len(bh)} days, costs {COST:.2%} per side)", "",
             shown.fillna("").to_markdown(), "",
             "## In-sample vs out-of-sample Sharpe of the chosen settings (mean across windows)", "",
             gap.round(2).to_markdown(), "",
             "## Cost sensitivity (out-of-sample Sharpe)", "", sens.round(2).to_markdown(), ""]
    (OUT / "RESULTS.md").write_text("\n".join(lines))
    print("\n".join(lines))

    # chart: out-of-sample equity curves (log scale) and drawdowns
    fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [3, 1]})
    for (k, r), c in zip(curves.items(), ["black", "tab:blue", "tab:orange", "tab:green"]):
        eq = np.exp(r.cumsum())
        ax[0].plot(eq.index, eq, label=k, color=c, lw=1.6 if k.startswith("Buy") else 1.2,
                   ls="--" if k.startswith("Buy") else "-")
        ax[1].plot(eq.index, (eq / eq.cummax() - 1) * 100, color=c, lw=1)
    ax[0].set_yscale("log"); ax[0].set_ylabel("Growth of $1 (log scale)")
    ax[0].set_title("Out-of-sample: walk-forward strategies vs buy-and-hold BTC, after 0.15% costs per side")
    ax[0].legend(); ax[0].grid(alpha=0.3); ax[1].set_ylabel("Drawdown (%)"); ax[1].grid(alpha=0.3)
    plt.tight_layout(); plt.savefig(OUT / "oos_equity.png", dpi=150)

    # Cross-check with the event-driven Portfolio simulator (backtesting/event_driven.py).
    # It acts one day later: it sees today's position and trades at today's close, so it is slightly
    # more conservative than the vectorised version, which trades at the close the signal is computed on.
    from backtesting.event_driven import run_backtest
    check = ["## Cross-check: event-driven simulator (trades one day later), same positions", "",
             "| Strategy | Vectorised Sharpe | Event-driven Sharpe | Event-driven total return |", "|---|---|---|---|"]
    for name in GRIDS:
        pos, r, _ = walk_forward(px, name, COST)
        frame = px.loc[pos.index, ["close"]].assign(position=pos)
        _, eq = run_backtest(frame, initial_cash=10_000, commission=0.001, slippage=0.0005)
        dr = np.log(eq["equity"]).diff().dropna()
        check.append(f"| {name} | {sharpe(r):.2f} | {sharpe(dr):.2f} | {eq['equity'].iloc[-1] / 10_000 - 1:+.1%} |")
    with open(OUT / "RESULTS.md", "a") as fh:
        fh.write("\n".join(check) + "\n")
    print("\n".join(check))


if __name__ == "__main__":
    main()
