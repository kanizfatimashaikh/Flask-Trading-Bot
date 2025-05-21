from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)

    symbol = data.get('symbol')
    signal = data.get('signal')

    if symbol and signal:
        print(f"Trade signal received: {signal} {symbol}")
        return jsonify({
            "received": {
                "symbol": symbol,
                "signal": signal
            },
            "status": "success"
        })
    else:
        return jsonify({"error": "Missing symbol or signal"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
