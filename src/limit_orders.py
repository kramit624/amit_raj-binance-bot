from binance.client import Client

def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float):
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )
        return order
    except Exception as e:
        return {"error": str(e)}
