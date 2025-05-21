from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Initialize or load state
STATE_FILE = "paper_trade_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "capital": 100000.0,
            "holdings": {},  # Format: { "RELIANCE": {"qty": 1, "buy_price": 2500.0} }
            "trade_log": [],
            "pnl": 0.0
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

# Dummy price fetcher (use real API if needed)
def get_dummy_price(symbol):
    dummy_prices = {
        "RELIANCE": 2500,
        "TCS": 3600,
        "INFY": 1450,
        "HDFCBANK": 1500
    }
    return dummy_prices.get(symbol.upper(), 1000)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signal = data.get("signal")
    symbol = data.get("symbol")
    if not symbol or not signal:
        return jsonify({"status": "error", "message": "Missing symbol or signal"}), 400

    state = load_state()
    capital = state["capital"]
    holdings = state["holdings"]
    log = state["trade_log"]
    price = get_dummy_price(symbol)
    qty = 1  # simulate buying 1 lot

    if signal.upper() == "BUY":
        cost = price * qty
        if capital >= cost:
            if symbol in holdings:
                return jsonify({"status": "error", "message": f"Already holding {symbol}"}), 400
            holdings[symbol] = {"qty": qty, "buy_price": price}
            state["capital"] -= cost
            log.append({
                "time": datetime.now().isoformat(),
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": qty,
                "capital": state["capital"]
            })
        else:
            return jsonify({"status": "error", "message": "Insufficient capital"}), 400

    elif signal.upper() == "SELL":
        if symbol not in holdings:
            return jsonify({"status": "error", "message": f"Not holding {symbol}"}), 400
        buy_price = holdings[symbol]["buy_price"]
        pnl = (price - buy_price) * qty
        state["pnl"] += pnl
        state["capital"] += price * qty
        del holdings[symbol]
        log.append({
            "time": datetime.now().isoformat(),
            "symbol": symbol,
            "action": "SELL",
            "price": price,
            "qty": qty,
            "pnl": pnl,
            "capital": state["capital"]
        })

    else:
        return jsonify({"status": "error", "message": "Unknown signal"}), 400

    save_state(state)
    return jsonify({"status": "success", "capital": state["capital"], "pnl": state["pnl"]})

@app.route("/status", methods=["GET"])
def status():
    state = load_state()
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

# Initialize or load state
STATE_FILE = "paper_trade_state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {
            "capital": 100000.0,
            "holdings": {},  # Format: { "RELIANCE": {"qty": 1, "buy_price": 2500.0} }
            "trade_log": [],
            "pnl": 0.0
        }
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

# Dummy price fetcher (use real API if needed)
def get_dummy_price(symbol):
    dummy_prices = {
        "RELIANCE": 2500,
        "TCS": 3600,
        "INFY": 1450,
        "HDFCBANK": 1500
    }
    return dummy_prices.get(symbol.upper(), 1000)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    signal = data.get("signal")
    symbol = data.get("symbol")
    if not symbol or not signal:
        return jsonify({"status": "error", "message": "Missing symbol or signal"}), 400

    state = load_state()
    capital = state["capital"]
    holdings = state["holdings"]
    log = state["trade_log"]
    price = get_dummy_price(symbol)
    qty = 1  # simulate buying 1 lot

    if signal.upper() == "BUY":
        cost = price * qty
        if capital >= cost:
            if symbol in holdings:
                return jsonify({"status": "error", "message": f"Already holding {symbol}"}), 400
            holdings[symbol] = {"qty": qty, "buy_price": price}
            state["capital"] -= cost
            log.append({
                "time": datetime.now().isoformat(),
                "symbol": symbol,
                "action": "BUY",
                "price": price,
                "qty": qty,
                "capital": state["capital"]
            })
        else:
            return jsonify({"status": "error", "message": "Insufficient capital"}), 400

    elif signal.upper() == "SELL":
        if symbol not in holdings:
            return jsonify({"status": "error", "message": f"Not holding {symbol}"}), 400
        buy_price = holdings[symbol]["buy_price"]
        pnl = (price - buy_price) * qty
        state["pnl"] += pnl
        state["capital"] += price * qty
        del holdings[symbol]
        log.append({
            "time": datetime.now().isoformat(),
            "symbol": symbol,
            "action": "SELL",
            "price": price,
            "qty": qty,
            "pnl": pnl,
            "capital": state["capital"]
        })

    else:
        return jsonify({"status": "error", "message": "Unknown signal"}), 400

    save_state(state)
    return jsonify({"status": "success", "capital": state["capital"], "pnl": state["pnl"]})

@app.route("/status", methods=["GET"])
def status():
    state = load_state()
    return jsonify(state)

if __name__ == "__main__":
    app.run(debug=True)
