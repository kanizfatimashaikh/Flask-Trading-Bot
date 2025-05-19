from flask import Flask, request
import datetime

app = Flask(__name__)

capital = 100000
lot_size = 500
open_trades = []
closed_trades = []

def get_option_price(stock_price, type_):
    base = stock_price * 0.05
    return round(base + (5 if type_ == 'CE' else 7), 2)

@app.route('/', methods=['POST'])
def webhook():
    global capital, open_trades, closed_trades
    data = request.json
    stock = data.get("stock")
    signal = data.get("signal")
    price = float(data.get("price", 0))

    if not stock or not signal or not price:
        return "Invalid data", 400

    option_type = "CE" if signal.upper() == "BUY" else "PE"
    strike_price = round(price * (1.02 if signal.upper() == "BUY" else 0.98))
    option_price = get_option_price(price, option_type)
    cost = option_price * lot_size

    if cost > capital:
        return f"Not enough capital. Available: ₹{capital}", 400

    trade = {
        "stock": stock.upper(),
        "signal": signal.upper(),
        "strike": strike_price,
        "option": f"{strike_price}{option_type}",
        "entry_price": option_price,
        "qty": lot_size,
        "entry_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    capital -= cost
    open_trades.append(trade)
    print(f"TRADE: {signal.upper()} {stock.upper()} {strike_price}{option_type} @ ₹{option_price} | Capital: ₹{capital}")
    simulate_trailing_profit()
    return "Trade Executed", 200

def simulate_trailing_profit():
    global open_trades, closed_trades, capital
    still_open = []
    for trade in open_trades:
        exit_price = round(trade["entry_price"] * 1.10, 2)
        pnl = (exit_price - trade["entry_price"]) * trade["qty"]
        capital += exit_price * trade["qty"]
        trade.update({
            "exit_price": exit_price,
            "exit_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "pnl": round(pnl, 2)
        })
        closed_trades.append(trade)
        print(f"CLOSED: {trade['stock']} {trade['option']} Entry ₹{trade['entry_price']} → Exit ₹{exit_price} | PnL ₹{pnl}")
    open_trades = still_open

@app.route('/report', methods=['GET'])
def report():
    return {
        "capital": capital,
        "open_trades": open_trades,
        "closed_trades": closed_trades
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
