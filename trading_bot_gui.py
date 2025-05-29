import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit, QVBoxLayout, QHBoxLayout, QTabWidget, QComboBox, QSpinBox, QMessageBox)
from bot import TradingBot
from strategies import SimpleStrategy, SmartStrategy
from utils import log_action
import threading

class LoginWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.api_key_input = QLineEdit()
        self.api_secret_input = QLineEdit()
        self.api_secret_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.login)

        layout.addWidget(QLabel("API Key"))
        layout.addWidget(self.api_key_input)
        layout.addWidget(QLabel("API Secret"))
        layout.addWidget(self.api_secret_input)
        layout.addWidget(login_button)
        self.setLayout(layout)

    def login(self):
        api_key = self.api_key_input.text()
        api_secret = self.api_secret_input.text()
        if api_key and api_secret:
            self.parent.api_key = api_key
            self.parent.api_secret = api_secret
            self.parent.show_main()
        else:
            QMessageBox.warning(self, "Error", "API credentials are required")

class BotControlWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.strategy_selector = QComboBox()
        self.strategy_selector.addItems(["Simple", "Smart"])

        self.buy_threshold = QSpinBox()
        self.buy_threshold.setValue(10)
        self.sell_threshold = QSpinBox()
        self.sell_threshold.setValue(10)

        start_btn = QPushButton("Start Bot")
        start_btn.clicked.connect(self.start_bot)

        layout.addWidget(QLabel("Strategy"))
        layout.addWidget(self.strategy_selector)
        layout.addWidget(QLabel("Buy Threshold % (Simple)"))
        layout.addWidget(self.buy_threshold)
        layout.addWidget(QLabel("Sell Threshold % (Simple)"))
        layout.addWidget(self.sell_threshold)
        layout.addWidget(start_btn)
        layout.addWidget(QLabel("Log"))
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def log(self, msg):
        log_action(self.log_output, msg)

    def start_bot(self):
        strat_name = self.strategy_selector.currentText()
        if strat_name == "Simple":
            strategy = SimpleStrategy(
                buy_threshold=self.buy_threshold.value() / 100,
                sell_threshold=self.sell_threshold.value() / 100
            )
        else:
            from backtest import load_data
            df = load_data()
            strategy = SmartStrategy(df)

        bot = TradingBot(self.parent.api_key, self.parent.api_secret, strategy)
        thread = threading.Thread(target=bot.run, args=(self.log,), daemon=True)
        thread.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_key = None
        self.api_secret = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Binance Trading Bot")
        self.login_widget = LoginWidget(self)
        self.setCentralWidget(self.login_widget)

    def show_main(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(BotControlWidget(self), "Live Trading")
        self.setCentralWidget(self.tabs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())