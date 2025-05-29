import pandas as pd
from strategies import GridStrategy
import matplotlib.pyplot as plt

class RollingGridBacktester:
    def __init__(self, df, strategy_config, window_days=30, step_days=15, budget_usd=1000):
        self.df = df
        self.strategy_config = strategy_config
        self.window_days = window_days
        self.step_days = step_days
        self.initial_budget = budget_usd
        self.results = []

    def run(self):
        start = 0
        while start + self.window_days <= len(self.df):
            sub_df = self.df.iloc[start:start + self.window_days].copy()
            strategy = GridStrategy(**self.strategy_config)
            budget = self.initial_budget
            coin = 0
            trades = []

            for _, row in sub_df.iterrows():
                price = row["close"]

                if strategy.should_buy(price):
                    amount = budget * 0.2
                    if amount > 10:
                        quantity = amount / price
                        coin += quantity
                        budget -= amount
                        strategy.on_buy(price, quantity)
                        trades.append((row["date"], "BUY", price))

                elif coin > 0 and strategy.should_sell(price):
                    value = coin * price
                    budget += value
                    strategy.on_sell()
                    trades.append((row["date"], "SELL", price))
                    coin = 0

                elif coin > 0 and strategy.should_exit(price):
                    value = coin * price
                    budget += value
                    strategy.on_sell()
                    trades.append((row["date"], "FORCED EXIT", price))
                    coin = 0

            final_price = sub_df["close"].iloc[-1]
            final_value = budget + coin * final_price
            net_profit = final_value - self.initial_budget
            self.results.append({
                "start": sub_df["date"].iloc[0],
                "end": sub_df["date"].iloc[-1],
                "profit": net_profit,
                "final_value": final_value,
                "trades": trades
            })

            start += self.step_days

    def report(self):
        print(f"📊 Rolling Window Backtest Report ({len(self.results)} runs)")
        print("--------------------------------------------------")
        total_profit = 0
        for i, result in enumerate(self.results):
            print(f"Run {i+1}: {result['start'].date()} → {result['end'].date()} | Profit: ${result['profit']:.2f} | Trades: {len(result['trades'])}")
            total_profit += result["profit"]
        print("--------------------------------------------------")
        print(f"Total Profit: ${total_profit:.2f}")
        self.plot()

    def plot(self):
        periods = [f"{r['start'].strftime('%Y-%m')}" for r in self.results]
        profits = [r['profit'] for r in self.results]
        plt.figure(figsize=(14, 5))
        plt.bar(periods, profits, color=["green" if p >= 0 else "red" for p in profits])
        plt.xticks(rotation=45)
        plt.title("Rolling Grid Strategy Monthly Profits")
        plt.ylabel("Net Profit ($)")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def load_data(filepath="btc_usdt_5y.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df.sort_values("date", inplace=True)
    return df

if __name__ == "__main__":
    df = load_data()
    strategy_config = {
        "grid_size": 0.05,
        "max_levels": 20,
        "max_drawdown": 0.30
    }
    backtester = RollingGridBacktester(df, strategy_config, window_days=30, step_days=15)
    backtester.run()
    backtester.report()
