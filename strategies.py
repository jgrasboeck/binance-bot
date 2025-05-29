class AdaptiveDCARecoveryStrategy:
    def __init__(self, buy_threshold=0.10, sell_threshold=0.10, max_drawdown=0.30):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.max_drawdown = max_drawdown
        self.reset()

    def reset(self):
        self.buy_prices = []
        self.total_invested = 0
        self.total_quantity = 0
        self.last_action_price = None

    def average_price(self):
        return self.total_invested / self.total_quantity if self.total_quantity > 0 else None

    def should_buy(self, current_price):
        if not self.buy_prices:
            return True  # First entry

        last_price = self.buy_prices[-1]
        dip = (last_price - current_price) / last_price
        return dip >= self.buy_threshold

    def should_sell(self, current_price):
        avg_price = self.average_price()
        if not avg_price:
            return False

        gain = (current_price - avg_price) / avg_price
        return gain >= self.sell_threshold

    def should_exit(self, current_price):
        avg_price = self.average_price()
        if not avg_price:
            return False

        loss = (avg_price - current_price) / avg_price
        return loss >= self.max_drawdown

    def on_buy(self, price, quantity):
        self.buy_prices.append(price)
        self.total_quantity += quantity
        self.total_invested += price * quantity

    def on_sell(self):
        self.reset()


class GridStrategy:
    def __init__(self, grid_size=0.10, max_levels=5, max_drawdown=0.30):
        self.grid_size = grid_size
        self.max_levels = max_levels
        self.max_drawdown = max_drawdown
        self.reset()

    def reset(self):
        self.positions = []
        self.total_invested = 0
        self.total_quantity = 0
        self.base_price = None

    def average_price(self):
        return self.total_invested / self.total_quantity if self.total_quantity > 0 else 0

    def should_buy(self, current_price):
        if not self.positions:
            return True
        last_price = self.positions[-1][0]
        return (last_price - current_price) / last_price >= self.grid_size

    def should_sell(self, current_price):
        if not self.positions:
            return False
        avg_price = self.average_price()
        return (current_price - avg_price) / avg_price >= self.grid_size

    def should_exit(self, current_price):
        if not self.positions:
            return False
        avg_price = self.average_price()
        return (avg_price - current_price) / avg_price >= self.max_drawdown

    def on_buy(self, price, quantity):
        self.positions.append((price, quantity))
        self.total_quantity += quantity
        self.total_invested += price * quantity

    def on_sell(self):
        self.reset()