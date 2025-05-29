# 🪙 Binance Trading Bot

This is a simple automated trading bot for Binance. It can buy and sell cryptocurrencies based on predefined rules. **No coding experience is required** to use this bot if you follow this guide.

---

## ⚠️ Disclaimer

> This bot trades with real money. Use at your own risk. The developer is not responsible for any financial losses. Always test with small amounts or in Binance’s testnet before using real funds.

---

## 🛠️ Requirements

Before starting, you'll need the following:

* A Binance account: [Sign up here](https://www.binance.com)
* Binance API keys (we’ll explain this below)
* A computer with:

  * [Python](https://www.python.org/downloads/) installed
  * Git installed (optional)
  * Terminal / Command Prompt access

---

## 🔑 How to Get Your Binance API Keys

1. Log in to your Binance account.
2. Go to **[API Management](https://www.binance.com/en/my/settings/api-management)**.
3. Create a new API key (e.g., name it "bot").
4. Save your **API Key** and **Secret Key** somewhere safe.
5. Make sure you enable **trading permissions** (but NOT withdrawals).

---

## 🔧 Installation Guide (Step-by-Step)

### Windows or Mac

#### 1. Download the Bot

Option 1: If using Git:

```bash
git clone https://github.com/YOUR_USERNAME/binance-bot.git
cd binance-bot
```

Option 2: Download ZIP

* Go to the GitHub repo
* Click "Code" → "Download ZIP"
* Unzip and open the folder

#### 2. Install Python Dependencies

Open a terminal in the project folder and run:

```bash
pip install -r requirements.txt
```

> This will install the necessary packages like `python-binance`.

#### 3. Create Your Configuration File

In the same folder, create a file called `.env` with the following content:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here
SYMBOL=BTCUSDT
TRADE_AMOUNT=0.001
```

* Replace `your_api_key_here` and `your_secret_key_here` with your Binance keys.
* `SYMBOL` is the coin you want to trade (e.g., `ETHUSDT`, `BTCUSDT`, etc.)
* `TRADE_AMOUNT` is how much of the coin you want to buy or sell per trade.

---

## ▶️ How to Run the Bot

In your terminal, type:

```bash
python bot.py
```

This will:

* Connect to Binance
* Monitor prices (depending on your strategy)
* Automatically place trades

You should see messages printed as the bot works (e.g., "BUY executed", "SELL executed").

---

## 🔄 What Does the Bot Actually Do?

The strategy depends on how you or the developer configured it, but common functions include:

* Monitor price changes
* Automatically buy when prices drop
* Automatically sell when prices rise
* Print logs of each trade

*You can tweak the rules inside `bot.py` if you're comfortable with simple code edits.*

---

## 🔢 Backtesting Features

Before risking real money, you can **backtest** the bot's performance using historical data. This helps you understand if your strategy would have worked in the past.

### How to Use Backtesting

1. Run the backtest script:

```bash
python backtest.py
```

2. The bot will simulate your trading logic using historical data for the specified coin (e.g., `BTCUSDT`).

3. You'll see:

* Total trades made
* Winning vs losing trades
* Final profit/loss

### Configuring Backtest Parameters

Edit `backtest.py` to adjust:

* Time range (e.g., last 30 days)
* Strategy logic
* Initial balance

This feature is great for:

* Testing strategies before using real funds
* Understanding market behavior
* Reducing risk

---

## 📁 Files Explained

* `bot.py` — The main bot script
* `backtest.py` — Simulates your strategy on historical data
* `requirements.txt` — List of required Python packages
* `.env` — Your personal settings (API keys, trading info)
* `README.md` — This file you're reading!

---

## 🦯 Test Before Real Use (Optional but Recommended)

Want to avoid risking real money?

You can:

1. Use Binance **testnet** (requires some setup)
2. Modify the bot to **simulate trades** (e.g., print only, no real buying/selling)

Ask for help if you want to set up a test mode!

---

## 📞 Need Help?

If you're stuck:

* Ask a tech-savvy friend to help with the setup
* Reach out via the GitHub "Issues" tab
* Open an issue describing your problem and error messages

---

## 💡 Future Ideas (Optional for Developer)

* Add a GUI for easy configuration
* Add support for more indicators (e.g., RSI, MACD)
* Add email or Telegram alerts
* Use SQLite or JSON to log past trades

---

## ✅ Summary

| Step | Description                      |
| ---- | -------------------------------- |
| 1    | Get Binance API keys             |
| 2    | Download this project            |
| 3    | Install Python + dependencies    |
| 4    | Create `.env` with your settings |
| 5    | Run `python bot.py`              |

That's it! 🚀
