import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from strategies import GridStrategy
import random

class MonteCarloGridSimulator:
    def __init__(self, df, strategy_config, window_days=30, simulations=1000, budget_usd=1000):
        self.df = df
        self.strategy_config = strategy_config
        self.window_days = window_days
        self.simulations = simulations
        self.initial_budget = budget_usd
        self.results = []

    def simulate_once(self, start_idx):
        sub_df = self.df.iloc[start_idx:start_idx + self.window_days].copy()
        strategy = GridStrategy(**self.strategy_config)
        budget = self.initial_budget
        coin = 0

        for _, row in sub_df.iterrows():
            price = row["close"]

            if strategy.should_buy(price):
                amount = budget * 0.2
                if amount > 10:
                    quantity = amount / price
                    coin += quantity
                    budget -= amount
                    strategy.on_buy(price, quantity)

            elif coin > 0 and strategy.should_sell(price):
                budget += coin * price
                strategy.on_sell()
                coin = 0

            elif coin > 0 and strategy.should_exit(price):
                budget += coin * price
                strategy.on_sell()
                coin = 0

        final_price = sub_df["close"].iloc[-1]
        final_value = budget + coin * final_price
        return final_value - self.initial_budget

    def run(self):
        max_start = len(self.df) - self.window_days
        for i in range(self.simulations):
            start_idx = random.randint(0, max_start)
            profit = self.simulate_once(start_idx)
            self.results.append(profit)

    def report(self):
        profits = np.array(self.results)
        mean = profits.mean()
        median = np.median(profits)
        win_rate = (profits > 0).mean() * 100

        print("\n📊 Monte Carlo Grid Strategy ROI Analysis")
        print("----------------------------------------")
        print(f"Simulations:     {self.simulations}")
        print(f"Avg ROI:         ${mean:.2f}")
        print(f"Median ROI:      ${median:.2f}")
        print(f"Win Rate:        {win_rate:.2f}%")
        print(f"Worst Loss:      ${profits.min():.2f}")
        print(f"Best Gain:       ${profits.max():.2f}")

        plt.hist(profits, bins=40, edgecolor='k', color='skyblue')
        plt.axvline(mean, color='green', linestyle='--', label=f"Mean (${mean:.2f})")
        plt.axvline(median, color='orange', linestyle='--', label=f"Median (${median:.2f})")
        plt.title("Monte Carlo ROI Distribution")
        plt.xlabel("Profit/Loss ($)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    df = pd.read_csv("btc_usdt_5y.csv", parse_dates=["date"])
    df.sort_values("date", inplace=True)

    strategy_config = {
        "grid_size": 0.10,
        "max_levels": 5,
        "max_drawdown": 0.30
    }

    simulator = MonteCarloGridSimulator(
        df=df,
        strategy_config=strategy_config,
        window_days=30,
        simulations=500,
        budget_usd=10000
    )

    simulator.run()
    simulator.report()
