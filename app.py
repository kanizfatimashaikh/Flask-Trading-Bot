from flask import Flask, request, jsonify
import pandas as pd
import ta
import datetime
import random

app = Flask(__name__)

capital = 100000  # Starting capital
profit = 0
trade_history = []

def calculate_indicators(df):
    df['ema_5'] = ta.trend.ema_indicator(df['close'], window=5).ema_indicator()
    df['ema_20'] = ta.trend.ema_indicator(df['close'], window=20).ema_indicator()
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd_diff()
    return df

def generate_signal(df):
    latest = df.iloc[-1]
    if latest['ema_5'] > latest['ema_20'] and latest['rsi'] > 60 and latest['macd'] > 0:
        return "BUY"
    elif latest['ema_5'] < latest['ema_20'] and latest['rsi'] < 40 and latest['macd'] < 0:
        return "SELL"
    return None

def simulate_trade(stock_price, signal, stock_name):
    global capital, profit

    option_type = "CE" if signal == "BUY" else "PE"
    strike_price = round(stock_price * (1.05 if signal == "BUY" else 0.95), -1)
    option_price = round(random.uniform(10, 25), 2)
    lot_size = 500
    total_cost = option_price * lot_size

    if total_cost > capital:
        return None

    capital -= total_cost
    exit_price = option_price * 1.1
    pl = (exit_price - option_price) * lot_size
    capital += total_cost + pl
    profit += pl

    trade = {
        "time": str(datetime.datetime.now()),
        "stock": stock_name,
        "signal": signal,
        "option": f"{strike_price}{option_type}",
        "entry_price": option_price,
        "exit_price": round(exit_price, 2),
        "P&L": round(pl, 2),
        "capital": round(capital, 2)
    }
    trade_history.append(trade)
    return trade

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    stock_name = data['stock']
    df = pd.DataFrame(data['ohlcv'])
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']

    df = calculate_indicators(df)
    signal = generate_signal(df)

    if signal:
        trade = simulate_trade(df['close'].iloc[-1], signal, stock_name)
        if trade:
            return jsonify({"status": "Trade executed", "details": trade})
        else:
            return jsonify({"status": "Insufficient capital, trade skipped"})
    else:
        return jsonify({"status": "No valid signal"})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "Total Profit": round(profit, 2),
        "Capital Remaining": round(capital, 2),
        "Recent Trades": trade_history[-10:]
    })

if __name__ == '__main__':
    app.run(debug=True)
