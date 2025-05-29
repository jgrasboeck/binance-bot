import pandas as pd
import matplotlib.pyplot as plt
from strategies import AdaptiveDCARecoveryStrategy

class Backtester:
    def __init__(self, df, strategy, budget_usd=1000):
        self.df = df
        self.strategy = strategy
        self.initial_budget = budget_usd
        self.budget = budget_usd
        self.coin = 0
        self.trades = []
        self.final_value = budget_usd

    def run(self):
        print("🔄 Starting backtest simulation...\n")
        for _, row in self.df.iterrows():
            price = row["close"]
            date = row["date"]

            # Buying logic
            if self.strategy.should_buy(price):
                amount_to_invest = self.budget * 0.5
                if amount_to_invest > 10:
                    quantity = amount_to_invest / price
                    self.coin += quantity
                    self.budget -= amount_to_invest
                    self.strategy.on_buy(price, quantity)
                    self.trades.append((date, "BUY", price))
                    print(f"[{date}] BUY  | +{quantity:.6f} BTC at ${price:.2f} | USD left: ${self.budget:.2f}")

            # Selling logic
            elif self.strategy.should_sell(price):
                proceeds = self.coin * price
                self.budget += proceeds
                self.strategy.on_sell()
                self.trades.append((date, "SELL", price))
                print(f"[{date}] SELL | -{self.coin:.6f} BTC at ${price:.2f} | USD now: ${self.budget:.2f}")
                self.coin = 0

            # Emergency exit
            elif self.strategy.should_exit(price):
                proceeds = self.coin * price
                self.budget += proceeds
                self.strategy.on_sell()
                self.trades.append((date, "FORCED EXIT", price))
                print(f"[{date}] FORCED EXIT | -{self.coin:.6f} BTC at ${price:.2f} | USD now: ${self.budget:.2f}")
                self.coin = 0

        self.final_value = self.budget + self.coin * self.df["close"].iloc[-1]
        print("\n✅ Simulation complete.\n")

    def report(self):
        print("====== 📊 BACKTEST SUMMARY ======")
        print(f"Initial budget:   ${self.initial_budget:.2f}")
        print(f"Final value:      ${self.final_value:.2f}")
        print(f"Net profit:       ${self.final_value - self.initial_budget:.2f}")
        print(f"Trades executed:  {len(self.trades)}")
        print(f"USD balance:      ${self.budget:.2f}")
        print(f"BTC balance:      {self.coin:.6f}")
        print("---------------------------------")
        print("Trade log:")
        for d, action, price in self.trades:
            print(f"  [{d}] {action:12} at ${price:.2f}")
        print("=================================\n")
        self.plot_trades()

    def plot_trades(self):
        df = self.df.copy()
        df["signal"] = ""
        for d, action, price in self.trades:
            match = df["date"] == d
            df.loc[match, "signal"] = action

        plt.figure(figsize=(14, 6))
        plt.plot(df["date"], df["close"], label="BTC/USDT Price", color="black", alpha=0.4, zorder=1)
        buys = df[df["signal"] == "BUY"]
        sells = df[df["signal"] == "SELL"]
        exits = df[df["signal"] == "FORCED EXIT"]
        plt.scatter(buys["date"], buys["close"], marker="^", color="green", label="BUY")
        plt.scatter(sells["date"], sells["close"], marker="v", color="blue", label="SELL")
        plt.scatter(exits["date"], exits["close"], marker="x", color="red", label="FORCED EXIT")
        plt.legend()
        plt.title("Strategy Backtest: Adaptive DCA Recovery")
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.grid()
        plt.tight_layout()
        plt.show()

def load_data(filepath="btc_usdt_1y.csv"):
    df = pd.read_csv(filepath, parse_dates=["date"])
    df.sort_values("date", inplace=True)
    return df

if __name__ == "__main__":
    df = load_data()
    strategy = AdaptiveDCARecoveryStrategy(
        buy_threshold=0.05,    # Buy again if price dips 5% from last buy
        sell_threshold=0.10,   # Sell if price is 10% above average buy
        max_drawdown=0.30      # Force-sell if price drops 30% below avg
    )
    backtester = Backtester(df, strategy)
    backtester.run()
    backtester.report()
