import pandas as pd
import matplotlib.pyplot as plt
from strategies import GridStrategy

class Backtester:
    def __init__(self, df, strategy, budget_usd=10000):
        self.df = df
        self.strategy = strategy
        self.initial_budget = budget_usd
        self.budget = budget_usd
        self.coin = 0
        self.trades = []
        self.final_value = budget_usd

    def run(self):
        for _, row in self.df.iterrows():
            price = row["close"]

            # Buy level
            if self.strategy.should_buy(price):
                amount = self.budget * 0.2  # Invest 20% per grid step
                if amount > 10:
                    quantity = amount / price
                    self.coin += quantity
                    self.budget -= amount
                    self.strategy.on_buy(price, quantity)
                    self.trades.append((row["date"], "BUY", price))

            # Sell level
            elif self.coin > 0 and self.strategy.should_sell(price):
                value = self.coin * price
                self.budget += value
                self.strategy.on_sell()
                self.trades.append((row["date"], "SELL", price))
                self.coin = 0

            # Exit condition
            elif self.coin > 0 and self.strategy.should_exit(price):
                value = self.coin * price
                self.budget += value
                self.strategy.on_sell()
                self.trades.append((row["date"], "FORCED EXIT", price))
                self.coin = 0

        self.final_value = self.budget + self.coin * self.df["close"].iloc[-1]

    def report(self):
        print("📊 Grid Strategy Backtest Summary")
        print("---------------------------------")
        print(f"Initial budget:  ${self.initial_budget:.2f}")
        print(f"Final value:     ${self.final_value:.2f}")
        print(f"Net profit:      ${self.final_value - self.initial_budget:.2f}")
        print(f"Trades executed: {len(self.trades)}")
        print()
        for d, action, price in self.trades:
            pass
            # print(f"{d} - {action} at ${price:.2f}")
        self.plot_trades()

    def plot_trades(self):
        df = self.df.copy()
        df["signal"] = ""
        for d, action, price in self.trades:
            df.loc[df["date"] == d, "signal"] = action

        plt.figure(figsize=(14, 6))
        plt.plot(df["date"], df["close"], label="BTC/USDT Price")
        for label, color, marker in [("BUY", "green", "^"), ("SELL", "blue", "v"), ("FORCED EXIT", "red", "x")]:
            points = df[df["signal"] == label]
            plt.scatter(points["date"], points["close"], marker=marker, color=color, label=label)

        plt.title("Grid Strategy Backtest")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

def load_data(filepath="btc_usdt_5y.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df.sort_values("date", inplace=True)
    return df

if __name__ == "__main__":
    df = load_data()
    strategy = GridStrategy(
        grid_size=0.05,        # 10% price step
        max_levels=20,          # Unused here but supports config
        max_drawdown=1.0      # Stop loss
    )
    backtester = Backtester(df, strategy)
    backtester.run()
    backtester.report()
