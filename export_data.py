from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta

# Optional: insert your public API key & secret
client = Client()

symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_1DAY
end_time = datetime.now()
start_time = end_time - timedelta(days=365*5)

# Download candles
klines = client.get_historical_klines(
    symbol,
    interval,
    start_str=start_time.strftime("%d %b %Y %H:%M:%S"),
    end_str=end_time.strftime("%d %b %Y %H:%M:%S")
)

# Format data
df = pd.DataFrame(klines, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "number_of_trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
])

df["date"] = pd.to_datetime(df["timestamp"], unit='ms')
df["open"] = df["open"].astype(float)
df["high"] = df["high"].astype(float)
df["low"] = df["low"].astype(float)
df["close"] = df["close"].astype(float)
df["volume"] = df["volume"].astype(float)

# Only keep needed columns
df = df[["date", "open", "high", "low", "close", "volume"]]

# Save to CSV
df.to_csv("btc_usdt_5y.csv", index=False)

print("✅ Export complete: btc_usdt_1y.csv")
