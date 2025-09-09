from flask import Flask, render_template, request
from binance.client import Client
from config import API_KEY, API_SECRET
from logger import setup_logger

from market_orders import place_market_order
from limit_orders import place_limit_order

from advanced.stop_limit import place_stop_limit_order
from advanced.oco import place_oco_order
from advanced.twap import place_twap_order
from advanced.grid import place_grid_orders

setup_logger()

app = Flask(__name__)
client = Client(API_KEY, API_SECRET, testnet=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/place_order", methods=["POST"])
def place_order():
    symbol = request.form.get("symbol")
    side = request.form.get("side").upper()
    order_type = request.form.get("order_type")
    
    qty = request.form.get("qty")
    qty = float(qty) if qty else None
    
    # Initialize result
    result = None
    
    try:
        if order_type == "market":
            result = place_market_order(client, symbol, side, qty)
            
        elif order_type == "limit":
            price = float(request.form.get("price"))
            result = place_limit_order(client, symbol, side, qty, price)
            
        elif order_type == "stop_limit":
            stop_price = float(request.form.get("stop_price"))
            limit_price = float(request.form.get("limit_price"))
            result = place_stop_limit_order(client, symbol, side, qty, stop_price, limit_price)
            
        elif order_type == "oco":
            price1 = float(request.form.get("price1"))
            price2 = float(request.form.get("price2"))
            result = place_oco_order(client, symbol, side, qty, price1, price2)
            
        elif order_type == "twap":
            duration = int(request.form.get("duration"))
            parts = int(request.form.get("parts"))
            result = place_twap_order(client, symbol, side, qty, duration, parts)
            
        elif order_type == "grid":
            quantity_per_order = float(request.form.get("quantity_per_order"))
            low_price = float(request.form.get("low_price"))
            high_price = float(request.form.get("high_price"))
            grid_count = int(request.form.get("grid_count"))
            result = place_grid_orders(client, symbol, side, quantity_per_order, low_price, high_price, grid_count)
            
        else:
            result = {"error": "Unsupported order type"}

        if "error" in result:
            app.logger.error(f"{order_type.upper()} order failed: {result['error']}")
            return f"❌ Error: {result['error']}"
        else:
            app.logger.info(f"{order_type.upper()} order successful: {result}")
            return f"✅ Order placed successfully!<br><br>{result}"

    except Exception as e:
        app.logger.error(f"Exception during order: {str(e)}")
        return f"❌ Exception: {str(e)}"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print("Flask app is running at http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=port, debug=True)
