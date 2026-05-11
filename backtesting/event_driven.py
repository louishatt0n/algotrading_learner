import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

try:
    PROJECT_ROOT = Path(__file__).resolve().parents[1]
except NameError:
    cwd = Path.cwd().resolve()
    PROJECT_ROOT = cwd.parent if cwd.name == "backtesting" else cwd
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_loader import df as ohlc
from strategies import sma_crossover, momentum, mean_reversion


class Portfolio:
    """ 
    Tracks the state of a trading account.
    """

    def __init__(self, initial_cash = 10_000.0, commission = 0.001, slippage = 0.0005):
        """
        Parameters:
            initial_cash: initial cash balance in USDT
            commission: commission per trade (0.001 = 0.1%)
            slippage: slippage per trade (0.0005 = 0.05%)
        """

        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0.0 #BTC held in position
        self.commission = commission
        self.slippage = slippage
        self.trades = [] #List of trade events
        self.equity_curve = [] #Equity curve over time
    
    def buy(self, price, date):
        """Open a long position using all available cash."""
        if self.position > 0:
            return #already in position

        #Slippage: buy slightly above market price
        exec_price = price * (1 + self.slippage)

        #Deduct commission
        commission_cost = self.cash * self.commission
        btc_amount = (self.cash - commission_cost) / exec_price

        self.position = btc_amount
        self.cash = 0.0

        self.trades.append({
            "date": date,
            "action": "buy",
            "price": exec_price,
            "amount": btc_amount,
            "cost": commission_cost,
        })
    
    def sell(self, price, date):
        """Close a long position."""
        if self.position == 0:
            return #no position to sell

        #Slippage: sell slightly below market price
        exec_price = price * (1 - self.slippage)

        proceeds = self.position * exec_price
        commission_cost = proceeds * self.commission
        self.cash = proceeds - commission_cost
        self.position = 0.0

        self.trades.append({
            "date": date,
            "action": "sell",
            "price": exec_price,
            "amount": 0,
            "cost": commission_cost,
        })

    def total_equity(self, current_price):
        """Current portfolio value: cash + position at current price."""
        return self.cash + self.position * current_price
    
    def record(self, date, current_price):
        """Record the current state of the equity curve."""
        self.equity_curve.append({
            "date": date,
            "equity": self.total_equity(current_price),
        })
        
def run_backtest(df_strategy, initial_cash = 10_000.0, commission = 0.001, slippage = 0.0005):
    """ 
    Event-driven backtest of a strategy.

    Parameters:
        df_strategy: pandas DataFrame with a 'position' column
        initial_cash: starting capital
        commission: commission per trade
        slippage: slippage

    Returns:
        portfolio: Portfolio object with equity curve
        equity_df: Dataframe with equity curve
    """

    portfolio = Portfolio(initial_cash, commission, slippage)
    data = df_strategy.dropna(subset=["position"]).copy()

    for date, row in data.iterrows():
        price = row["close"]
        position = row["position"]

        if position == 1:
            portfolio.buy(price, date)
        elif position <= 0:
            portfolio.sell(price, date)
        
        portfolio.record(date, price)
    
    equity_df = pd.DataFrame(portfolio.equity_curve).set_index("date")
    return portfolio, equity_df

df_sma = sma_crossover.sma_crossover(ohlc, fast=20, slow=50)

portfolio, equity_df = run_backtest(df_sma, initial_cash=10_000)

print(f"Starting capital:  ${portfolio.initial_cash:,.0f}")
print(f"Final capital:     ${equity_df['equity'].iloc[-1]:,.0f}")
print(f"Number of trades:  {len(portfolio.trades)}")
print(f"Total commissions: ${sum(t['cost'] for t in portfolio.trades):,.2f}")


#Impact of Commissions and Slippage on Returns (SMA 20/50)
configs = [
    {"commission": 0.0,    "slippage": 0.0,    "label": "No costs"},
    {"commission": 0.001,  "slippage": 0.0,    "label": "Commission only (0.1%)"},
    {"commission": 0.001,  "slippage": 0.0005, "label": "Commission + slippage"},
    {"commission": 0.002,  "slippage": 0.001,  "label": "High costs"},
]

results = {}
for cfg in configs:
    _, eq = run_backtest(df_sma,
                         commission=cfg["commission"],
                         slippage=cfg["slippage"])
    results[cfg["label"]] = eq

fig, ax = plt.subplots(figsize=(12, 5))
for label, eq in results.items():
    ax.plot(eq.index, eq["equity"], label=label, linewidth=1.2)

ax.set_title("Impact of Commissions and Slippage on Returns (SMA 20/50)")
ax.set_ylabel("Capital (USDT)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

#Every strategy has parameters. For SMA crossover those are the fast and slow periods. The question is: which values produce the best results?
# One way to answer that is to try every combination and pick the best. This is called a grid search.

def grid_search_sma(ohlc, fast_range, slow_range, commission = 0.001):
    """ Iterate over all SMA crossover parameter combinations.
    Return a dataframe with the best results for each pair.
    """
    results = []

    for fast in fast_range:
        for slow in slow_range:
            if fast >= slow:
                continue #fast SMA must be shorter than slow SMA

            df_strat = sma_crossover.sma_crossover(ohlc, fast=fast, slow=slow)
            portfolio, equity_df = run_backtest(df_strat, commission=commission)

            final_equity = equity_df["equity"].iloc[-1]
            total_return = (final_equity / portfolio.initial_cash) - 1

            #Sharpe Ratio
            daily_returns = equity_df["equity"].pct_change().dropna()
            daily_vol = daily_returns.std()
            sharpe = (daily_returns.mean() / daily_vol) * np.sqrt(252) if daily_vol > 0 else 0
            
            #Maximum Drawdown
            rolling_max = equity_df["equity"].cummax()
            max_drawdown = ((equity_df["equity"] - rolling_max) / rolling_max).min()

            results.append({
                "fast": fast,
                "slow": slow,
                "total_return": total_return,
                "sharpe": sharpe,
                "max_drawdown": max_drawdown,
                "trades": len(portfolio.trades),
            })

    return pd.DataFrame(results).sort_values(by="sharpe", ascending=False)


#Run the search
fast_range = range(5, 51, 5) #5-51 days in 5-day spacing
slow_range = range(10, 101, 10) #10, 20, 30, 40 etc.

grid_results = grid_search_sma(ohlc, fast_range, slow_range, commission=0.001)
print(grid_results.head(10))

#Heatmap of the Result, visualising
import seaborn as sns

pivot = grid_results.pivot(index="slow", columns="fast", values="sharpe")

fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(pivot, annot=False, fmt=".2f", cmap="RdYlGn",
            center=0, ax=ax, cbar_kws={"label": "Sharpe ratio"})
ax.set_title("Sharpe Ratio: SMA Crossover (fast vs slow)")
ax.set_xlabel("Fast SMA (days)")
ax.set_ylabel("Slow SMA (days)")
plt.tight_layout()
plt.show()

#With financial data there is a key constraint: it is sequential. You cannot shuffle future data in with the past. The split must be strictly chronological. 
#Walk forward analysis is a more realistic version of the same principle. A window slides across the data 
#e.g., take a training window, (say 1 year), optimise parameters on it, test on the next window (e.g., 3 months, out-of-sample), shift both windows forward by 3 months.
# Repeat until the end of the data is reached.

def walk_forward_analysis(ohlc, fast_range, slow_range, train_months = 12, test_months = 3, commission = 0.001):
    """ Walk forward analysis of SMA crossover strategy.

    At each step:
    1. Optimise parameters on training window
    2. Record out-of-sample results on the test window
    """

    results_oos = []

    start = ohlc.index[0]
    end = ohlc.index[-1]

    window_start = start
    while True:
        train_end = window_start + pd.DateOffset(months=train_months)
        test_end = train_end + pd.DateOffset(months=test_months)

        if test_end > end:
            break

        df_train = ohlc.loc[window_start:train_end]
        df_test = ohlc.loc[train_end:test_end]

        if len(df_train) < 60 or len(df_test) < 10:
            window_start += pd.DateOffset(months=test_months)
            continue

        #Optimise on the Training set
        best_sharpe = -np.inf
        best_fast, best_slow = 20, 50

        for fast in fast_range:
            for slow in slow_range:
                if fast >= slow:
                    continue #fast SMA must be shorter than slow SMA
                df_s = sma_crossover.sma_crossover(df_train, fast=fast, slow=slow)
                _, eq = run_backtest(df_s, commission=commission)
                if len(eq) < 5:
                    continue #Too few trades
                dr = eq["equity"].pct_change().dropna()
                sharpe = (dr.mean() / dr.std()) * np.sqrt(252) if dr.std() > 0 else 0
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_fast, best_slow = fast, slow

        #Out-of-sample test
        df_s_test = sma_crossover.sma_crossover(df_test, fast=best_fast, slow=best_slow)
        _, eq_test = run_backtest(df_s_test, commission=commission)

        if len(eq_test) > 0:
            oos_return = (eq_test["equity"].iloc[-1] / eq_test["equity"].iloc[0]) - 1
            results_oos.append({
                "period_start": train_end.date(),
                "period_end": test_end.date(),
                "best_fast": best_fast,
                "best_slow": best_slow,
                "oos_return": oos_return,
            })

        window_start += pd.DateOffset(months=test_months)
    
    return pd.DataFrame(results_oos)

#Run walk-forward
fast_range_wf = range(10, 41, 10)
slow_range_wf = range(20, 101, 20)

wf_results = walk_forward_analysis(ohlc, fast_range_wf, slow_range_wf, train_months=12, test_months=3, commission=0.001)
print(wf_results.to_string())
print(f"\nAverage OOS return per quarter:  {wf_results['oos_return'].mean():.2%}")
print(f"Percentage of profitable quarters: {(wf_results['oos_return'] > 0).mean():.1%}")

def kelly_fraction(trades_df):
    """
    Computes the Kelly fraction from trade history.

    Parameters:
        trades_df -- DataFrame with trades (needs a 'pnl' column)

    Returns:
        kelly_f -- recommended fraction of capital (between 0 and 1)
    """
    wins   = trades_df[trades_df["pnl"] > 0]["pnl"]
    losses = trades_df[trades_df["pnl"] < 0]["pnl"].abs()

    if len(wins) == 0 or len(losses) == 0:
        return 0.0

    p = len(wins) / len(trades_df)      # win rate
    avg_win  = wins.mean()
    avg_loss = losses.mean()
    b = avg_win / avg_loss              # win/loss ratio

    kelly_f = (p * b - (1 - p)) / b
    return max(0.0, min(kelly_f, 1.0))  # clip to [0, 1]

def run_backtest_kelly(df_strategy, initial_cash=10_000.0,
                       commission=0.001, kelly_multiplier=0.5):
    """
    Event-driven backtest with Kelly-based position sizing.
    """
    portfolio = Portfolio(initial_cash, commission)
    data = df_strategy.dropna(subset=["position"]).copy()

    # First run a standard backtest to estimate Kelly parameters
    _, eq_base = run_backtest(df_strategy, initial_cash, commission)

    strategy_returns = eq_base["equity"].pct_change().dropna()
    in_position      = df_strategy["position"].reindex(eq_base.index).fillna(0)
    trade_returns    = strategy_returns[in_position == 1]

    if len(trade_returns) > 10:
        wins   = trade_returns[trade_returns > 0]
        losses = trade_returns[trade_returns < 0].abs()
        p      = len(wins) / len(trade_returns)
        b      = wins.mean() / losses.mean() if len(losses) > 0 else 1.0
        kelly_f = max(0.0, min((p * b - (1 - p)) / b, 1.0))
    else:
        kelly_f = 0.5  # default fallback

    fraction = kelly_f * kelly_multiplier
    print(f"Kelly fraction: {kelly_f:.2%}, using: {fraction:.2%} of capital")

    # Run the backtest with this fraction
    cash      = initial_cash
    position  = 0.0
    equity_curve = []

    for date, row in data.iterrows():
        price  = row["close"]
        signal = row["position"]

        if signal == 1 and position == 0:
            invest    = cash * fraction
            cost      = invest * commission
            position  = (invest - cost) / price
            cash     -= invest

        elif signal == 0 and position > 0:
            proceeds  = position * price
            cost      = proceeds * commission
            cash     += proceeds - cost
            position  = 0.0

        equity_curve.append({
            "date":   date,
            "equity": cash + position * price,
        })

    equity_df = pd.DataFrame(equity_curve).set_index("date")
    return equity_df, kelly_f