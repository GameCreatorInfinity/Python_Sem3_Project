from flask import Flask, render_template, request, jsonify
import urllib.request
import json

app = Flask(__name__)

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def get_rates():
    """Fetch latest exchange rates from API."""
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())
        return data["rates"], data["base"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.get_json()
        from_curr = data.get("from", "").upper()
        to_curr = data.get("to", "").upper()
        amount = float(data.get("amount", 0))

        rates, base = get_rates()

        if from_curr not in rates or to_curr not in rates:
            return jsonify({"error": "Invalid currency code"}), 400

        usd_amount = amount / rates[from_curr]
        converted = usd_amount * rates[to_curr]
        return jsonify({
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "converted": round(converted, 2),
            "rates": list(rates.keys())  # send currency list to frontend
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
