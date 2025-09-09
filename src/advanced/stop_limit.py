from binance.client import Client

def place_stop_limit_order(client: Client, symbol: str, side: str, quantity: float, stop_price: float, limit_price: float):
    """
    Places a stop-limit order on Binance Futures Testnet.
    """
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP",
            timeInForce="GTC",
            quantity=quantity,
            price=str(limit_price),
            stopPrice=str(stop_price)
        )
        return order
    except Exception as e:
        return {"error": str(e)}
