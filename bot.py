from binance.client import Client
import time
from strategies import AdaptiveDCARecoveryStrategy

class TradingBot:
    def __init__(self, api_key, api_secret, strategy, symbol="BTCUSDT", budget_usd=1000):
        self.client = Client(api_key, api_secret)
        self.strategy = strategy
        self.symbol = symbol
        self.budget = budget_usd
        self.coin = 0
        self.running = True

    def get_price(self):
        ticker = self.client.get_symbol_ticker(symbol=self.symbol)
        return float(ticker["price"])

    def run(self, log):
        log("🚀 Bot started")
        while self.running:
            try:
                price = self.get_price()
                log(f"Price: ${price:.2f}")

                if self.strategy.should_buy(price):
                    amount_to_invest = self.budget * 0.5
                    if amount_to_invest > 10:
                        quantity = amount_to_invest / price
                        self.coin += quantity
                        self.budget -= amount_to_invest
                        self.strategy.on_buy(price, quantity)
                        log(f"BUY: {quantity:.6f} @ ${price:.2f}")

                elif self.strategy.should_sell(price):
                    value = self.coin * price
                    self.budget += value
                    self.strategy.on_sell()
                    log(f"SELL: {self.coin:.6f} @ ${price:.2f} = ${value:.2f}")
                    self.coin = 0

                elif self.strategy.should_exit(price):
                    value = self.coin * price
                    self.budget += value
                    self.strategy.on_sell()
                    log(f"⚠️ FORCED EXIT: {self.coin:.6f} @ ${price:.2f} = ${value:.2f}")
                    self.coin = 0

            except Exception as e:
                log(f"Error: {str(e)}")

            time.sleep(60)  # wait 1 minute before next action

    def stop(self):
        self.running = False
