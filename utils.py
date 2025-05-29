from datetime import datetime

def log_action(widget, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    widget.append(f"[{timestamp}] {message}")
