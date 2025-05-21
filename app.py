from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Flask Trading Bot is Live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data is None:
        return jsonify({'error': 'Invalid data'}), 400

    # Example: Log received data
    print("Received webhook:", data)

    # Example response
    return jsonify({'status': 'success', 'received': data}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use PORT from Render
    app.run(host='0.0.0.0', port=port)
