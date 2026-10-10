import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import sys
from pathlib import Path

try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path.cwd().resolve()
    PROJECT_ROOT = cwd.parent if cwd.name == "backtesting" else cwd
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import load_prices, PERIODS_PER_YEAR
from strategies import sma_crossover, momentum, mean_reversion


def backtest(ohlc, strategy_name = "Strategy", cost_per_side = 0.0):
    """
    Vectorised backtest of a strategy.
    Parameters:
        ohlc: pandas DataFrame with OHLC data with 'log_return' and 'position' columns
        strategy_name: name of the strategy (for display)
        cost_per_side: trading cost per unit of position traded (0.0015 = 0.10% commission + 0.05% slippage)
    Returns: dict of metrics and a df with results
    """

    result = ohlc.copy().dropna(subset=["position", "log_return"])

    #Strategy return: market return multiplied by position
    result["strategy_return"] = result["log_return"] * result["position"]

    #Trading costs: pay cost_per_side on every unit of position traded (flat->long = 1 unit, short->long = 2 units)
    turnover = result["position"].diff().abs().fillna(result["position"].abs())
    result["strategy_return"] += np.log(1 - turnover * cost_per_side)

    #Cumulative return: Strategy vs buy-and-hold
    result["cumret_strategy"] = result["strategy_return"].cumsum().apply(np.exp)
    result["cumret_buyandhold"] = result["log_return"].cumsum().apply(np.exp)

    #Metrics
    total_return = result["cumret_strategy"].iloc[-1] - 1
    bh_return = result["cumret_buyandhold"].iloc[-1] - 1

    annual_return = (1 + total_return) ** (PERIODS_PER_YEAR / len(result)) - 1
    annual_vol = result["strategy_return"].std() * np.sqrt(PERIODS_PER_YEAR)
    sharpe = annual_return / annual_vol if annual_vol > 0 else 0

    #Maximum drawdown
    rolling_max = result["cumret_strategy"].cummax()
    drawdown = (result["cumret_strategy"] - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    #Win rate: share of days in the market (long or short) with a positive strategy return
    in_market = result["position"] != 0
    winning_days = ((result["strategy_return"] > 0) & in_market).sum()
    trading_days = in_market.sum()
    win_rate = winning_days / trading_days if trading_days > 0 else 0

    metrics = {
        "name": strategy_name,
        "total_return": total_return,
        "bh_return": bh_return,
        "annual_return": annual_return,
        "annual_vol": annual_vol,
        "sharpe": sharpe,
        "max_drawdown": max_drawdown,
        "win_rate": win_rate,
        "trading_days": trading_days,
    }

    return metrics, result
    


def print_metrics(metrics):
    print(f"\n{'=' * 45}")
    print(f"  {metrics['name']}")
    print(f"{'=' * 45}")
    print(f"  Strategy return:     {metrics['total_return']:>8.1%}")
    print(f"  Buy-and-hold return: {metrics['bh_return']:>8.1%}")
    print(f"  Annual return:       {metrics['annual_return']:>8.1%}")
    print(f"  Annual volatility:   {metrics['annual_vol']:>8.1%}")
    print(f"  Sharpe ratio:        {metrics['sharpe']:>8.2f}")
    print(f"  Max drawdown:        {metrics['max_drawdown']:>8.1%}")
    print(f"  Win rate:            {metrics['win_rate']:>8.1%}")
    print(f"  Days in market:      {metrics['trading_days']:>8}")


#Rough benchmark for Sharpe ratios
#- `Sharpe < 0.5` - weak strategy
#- `0.5 -- 1.0` - acceptable
#- `1.0 -- 2.0` - good
#- `> 2.0` - excellent (or a bug in the backtest)


def plot_equity_curves(results: dict):
    """
    results -- dict of {"Name": result_DataFrame}
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 9),
                              gridspec_kw={"height_ratios": [3, 1]})

    colors = ["steelblue", "darkorange", "forestgreen"]

    first_res = list(results.values())[0]
    axes[0].plot(first_res.index, first_res["cumret_buyandhold"],
                 linewidth=1.2, color="black", linestyle="--",
                 label="Buy & Hold", alpha=0.7)

    for (name, res), color in zip(results.items(), colors):
        axes[0].plot(res.index, res["cumret_strategy"],
                     linewidth=1.2, color=color, label=name)

    axes[0].set_title("Equity Curve: Strategies vs Buy & Hold (BTC/USDT)")
    axes[0].set_ylabel("Cumulative Return (start = 1)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    axes[0].axhline(1, color="gray", linewidth=0.6, linestyle=":")

    for (name, res), color in zip(results.items(), colors):
        rolling_max = res["cumret_strategy"].cummax()
        drawdown    = (res["cumret_strategy"] - rolling_max) / rolling_max
        axes[1].fill_between(res.index, 0, drawdown * 100,
                              alpha=0.4, color=color, label=name)

    axes[1].set_ylabel("Drawdown (%)")
    axes[1].set_xlabel("Date")
    axes[1].legend(loc="lower left", fontsize=8)
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()



def comparison_table(metrics_list):
    rows = []
    for m in metrics_list:
        rows.append({
            "Strategy":      m["name"],
            "Return":        f"{m['total_return']:+.1%}",
            "Buy & Hold":    f"{m['bh_return']:+.1%}",
            "Sharpe":        f"{m['sharpe']:.2f}",
            "Max Drawdown":  f"{m['max_drawdown']:.1%}",
            "Win Rate":      f"{m['win_rate']:.1%}",
            "Days in Market": m["trading_days"],
        })
    return pd.DataFrame(rows).set_index("Strategy")


if __name__ == "__main__":
    ohlc = load_prices()
    print(f"Period: {ohlc.index[0].date()} to {ohlc.index[-1].date()}")
    print(f"Total days: {len(ohlc)}")

    df_sma = sma_crossover.sma_crossover(ohlc, fast=20, slow=50)
    df_mom = momentum.momentum_strategy(ohlc, window=20)
    df_mr = mean_reversion.mean_reversion_strategy(ohlc, window=20, threshold=-1.0)

    COST = 0.0015  # 0.10% commission + 0.05% slippage per side, as in event_driven.py
    metrics_sma, res_sma = backtest(df_sma, "SMA Crossover (20/50)", COST)
    metrics_mom, res_mom = backtest(df_mom, "Momentum (20d)", COST)
    metrics_mr,  res_mr  = backtest(df_mr,  "Mean Reversion (20/-1)", COST)

    for m in [metrics_sma, metrics_mom, metrics_mr]:
        print_metrics(m)

    results = {
        "SMA Crossover (20/50)": res_sma,
        "Momentum (20d)":         res_mom,
        "Mean Reversion (20/-1)": res_mr,
    }
    #plot_equity_curves(results)

    table = comparison_table([metrics_sma, metrics_mom, metrics_mr])
    print(table.to_string())
